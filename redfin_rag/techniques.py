"""Build and query various indexing / retrieval techniques.

1. Parent-child vector index with the query router
2. LlamaIndex VectorStoreIndex persisted in Chroma
3. LlamaIndex TreeIndex (select_leaf)
4. LangChain Chroma similarity search
5. LangChain Chroma maximal marginal relevance search
"""

from __future__ import annotations

import os
import re
import shutil
import time
from dataclasses import dataclass, field

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from llama_index.core import StorageContext, TreeIndex, VectorStoreIndex, load_index_from_storage
from llama_index.core.vector_stores import FilterOperator, MetadataFilter, MetadataFilters
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

from redfin_rag.corpus import ROOT

CHROMA_LLAMA_PATH = ROOT / "chroma_db_storage"
CHROMA_LLAMA_COLLECTION = "redfin_specs_collection"
TREE_PERSIST_DIR = ROOT / "tree_graph_metadata"
LC_CHROMA_PATH = ROOT / "rag_vectorstore"
LC_CHROMA_COLLECTION = "func_reqs_rag"

_LIST_CUES = (
    "all ",
    "every ",
    "associated with",
    "ids associated",
    "functional requirements id",
    "acceptance criteria id",
    "requirement ids",
    "ac ids",
    "fr ids",
)


@dataclass
class Hit:
    text: str
    metadata: dict = field(default_factory=dict)
    score: float | None = None


@dataclass
class Technique:
    name: str
    description: str
    retrieve: callable
    rewrites_query: bool = False


def rewrite_query(user_query: str) -> str:
    """Rewrite a conversational query into a standalone search statement."""
    llm = ChatOpenAI(model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"), temperature=0.0)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a RAG search query optimizer.
            Your job is to rewrite conversational user queries into clean, standalone search statements
            optimized for an embedding model.

            STRICT CRITICAL RULES:
            1. Always preserve specific technical prefixes exactly as written,
            specifically 'FR-' (Functional Requirements) and 'AC-' (Acceptance Criteria). Never drop the hyphen or the codes.
            2. If the user mentions IDs generally (e.g., 'all FR ids' or 'AC codes'),
            explicitly include the prefix wildcards 'FR-' or 'AC-' in your rewrite to anchor vector matching.
            3. Ground the vector search by appending the exact formatting notations used in the documents: 'Functional Requirements FR-XXXX' and 'Acceptance Criteria AC-XXXX'.
            4. Output ONLY the rewritten search statement. Do not include introductory text, explanations, or quotes around the output.
            """,
            ),
            ("user", "{user_query}"),
        ]
    )
    response = (prompt | llm).invoke({"user_query": user_query})
    return response.content


class _RewriteCache:
    def __init__(self):
        self._cache: dict[str, str] = {}

    def __call__(self, query: str) -> str:
        if query not in self._cache:
            self._cache[query] = rewrite_query(query)
        return self._cache[query]


class ParentChildRetriever:
    """Header-2 vector search, plus the feature / single-requirement router.
    Router is the main function that determines the type of query and the appropriate retrieval method."""

    def __init__(self, parent_nodes, leaf_nodes, parent_by_id):
        self.parent_nodes = parent_nodes
        self.leaf_nodes = leaf_nodes
        self.parent_by_id = parent_by_id
        self.index = VectorStoreIndex(leaf_nodes, show_progress=False)
        self.retriever = self.index.as_retriever(similarity_top_k=4)

    def _pack(self, node, score=None) -> dict:
        parent_id = node.metadata.get("parent_id")
        return {"score": score, "leaf": node, "parent": self.parent_by_id.get(parent_id)}

    def retrieve_requirements(self, query: str, k: int = 4) -> list[dict]:
        self.retriever.similarity_top_k = k
        hits = self.retriever.retrieve(query)
        packed = []
        for hit in hits:
            parent_id = hit.node.metadata.get("parent_id")
            packed.append(
                {"score": hit.score, "leaf": hit.node, "parent": self.parent_by_id.get(parent_id)}
            )
        return packed

    def leaves_for_parent(self, parent_id: str) -> list[dict]:
        return [self._pack(node) for node in self.leaf_nodes if node.metadata.get("parent_id") == parent_id]

    def match_parent_from_query(self, query: str):
        lowered = query.lower()
        quoted = re.findall(r"['\"]([^'\"]+)['\"]", query)
        candidates = quoted + [query]
        for parent in self.parent_nodes:
            name = (parent.metadata.get("feature_name") or "").lower()
            header = (parent.metadata.get("Header 1") or "").lower()
            feature_id = str(parent.metadata.get("feature_id") or "")
            for candidate in candidates:
                text = candidate.lower().strip()
                if name and name in text:
                    return parent
                if header and header in text:
                    return parent
            if name and name in lowered:
                return parent
            if feature_id and re.search(rf"\bfeature\s*{re.escape(feature_id)}\b", lowered):
                return parent
        hits = self.retrieve_requirements(query, k=1)
        return hits[0]["parent"] if hits else None

    def retrieve_one_requirement(self, query: str, requirement_id=None, k: int = 4) -> list[dict]:
        if requirement_id:
            exact = [
                node
                for node in self.leaf_nodes
                if (node.metadata.get("requirement_id") or "").upper() == requirement_id.upper()
            ]
            if exact:
                return [self._pack(node, score=1.0) for node in exact]
            filtered = self.index.as_retriever(
                similarity_top_k=k,
                filters=MetadataFilters(
                    filters=[
                        MetadataFilter(
                            key="requirement_id",
                            value=requirement_id,
                            operator=FilterOperator.EQ,
                        )
                    ]
                ),
            )
            hits = filtered.retrieve(query)
            if hits:
                return [
                    {
                        "score": hit.score,
                        "leaf": hit.node,
                        "parent": self.parent_by_id.get(hit.node.metadata.get("parent_id")),
                    }
                    for hit in hits
                ]
        return self.retrieve_requirements(query, k=k)

    def route_retrieve(self, query: str, k: int = 4, rewrite=None) -> dict:
        route, extra = _classify_query(query)
        active_query = query
        rewritten = None
        if route == "ambiguous":
            rewritten = rewrite(query) if rewrite else query
            active_query = rewritten or query
            route, extra = _classify_query(active_query)
            if route == "ambiguous":
                route = "leaf_one"

        parent = None
        if route == "feature_all":
            parent = self.match_parent_from_query(active_query)
            parent_id = parent.metadata.get("parent_id") if parent is not None else None
            results = (
                self.leaves_for_parent(parent_id)
                if parent_id
                else self.retrieve_requirements(active_query, k=k)
            )
        else:
            results = self.retrieve_one_requirement(
                active_query, requirement_id=extra.get("requirement_id"), k=k
            )
            if results:
                parent = results[0].get("parent")
        return {
            "route": route,
            "query": query,
            "rewritten_query": rewritten,
            "parent": parent,
            "results": results,
        }


def _extract_ids(query: str):
    fr = re.search(r"FR-\d+", query, re.I)
    ac = re.search(r"AC-\d+(?:\.\d+)?", query, re.I)
    return (
        fr.group(0).upper() if fr else None,
        ac.group(0).upper() if ac else None,
    )


def _classify_query(query: str):
    fr_id, ac_id = _extract_ids(query)
    lowered = query.lower()
    wants_list = any(cue in lowered for cue in _LIST_CUES)
    extra = {"requirement_id": fr_id, "ac_id": ac_id}
    if (fr_id or ac_id) and not wants_list:
        return "leaf_one", extra
    if wants_list or ("feature" in lowered and not fr_id):
        return "feature_all", extra
    return "ambiguous", extra


def _hits_from_nodes(nodes) -> list[Hit]:
    hits = []
    for node in nodes:
        source = getattr(node, "node", node)
        text = getattr(source, "text", None) or getattr(source, "page_content", "")
        metadata = dict(getattr(source, "metadata", None) or {})
        score = getattr(node, "score", None)
        hits.append(Hit(text=text, metadata=metadata, score=score))
    return hits


def _hits_from_lc_docs(docs) -> list[Hit]:
    return [Hit(text=doc.page_content, metadata=dict(doc.metadata or {})) for doc in docs]


def _build_llama_chroma(feature_docs):
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_LLAMA_PATH))
    collection = chroma_client.get_or_create_collection(CHROMA_LLAMA_COLLECTION)
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    if collection.count() == 0:
        index = VectorStoreIndex.from_documents(feature_docs, storage_context=storage_context)
    else:
        index = VectorStoreIndex.from_vector_store(vector_store)
    return index


def _build_tree(feature_docs):
    if TREE_PERSIST_DIR.exists():
        storage_context = StorageContext.from_defaults(persist_dir=str(TREE_PERSIST_DIR))
        return load_index_from_storage(storage_context)
    index = TreeIndex.from_documents(feature_docs, num_children=8)
    index.storage_context.persist(str(TREE_PERSIST_DIR))
    return index


def _build_langchain_chroma(lc_docs):
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    persist_directory = str(LC_CHROMA_PATH)
    if os.path.exists(persist_directory):
        try:
            store = Chroma(
                collection_name=LC_CHROMA_COLLECTION,
                embedding_function=embeddings,
                persist_directory=persist_directory,
            )
            if store._collection.count() > 0:
                return store
        except Exception:
            store = None
        try:
            shutil.rmtree(persist_directory)
        except PermissionError:
            persist_directory = str(ROOT / f"rag_vectorstore_{int(time.time())}")
    return Chroma.from_documents(
        documents=lc_docs,
        embedding=embeddings,
        collection_name=LC_CHROMA_COLLECTION,
        persist_directory=persist_directory,
        collection_metadata={"hnsw:space": "cosine"},
    )


def build_techniques(corpus: dict, rewrite=None) -> list[Technique]:
    rewrite = rewrite or _RewriteCache()
    parent_child = ParentChildRetriever(
        corpus["parent_nodes"], corpus["leaf_nodes"], corpus["parent_by_id"]
    )
    vector_index = _build_llama_chroma(corpus["feature_docs"])
    tree_index = _build_tree(corpus["feature_docs"])
    chroma_store = _build_langchain_chroma(corpus["lc_docs"])

    def parent_child_retrieve(query: str, k: int) -> list[Hit]:
        routed = parent_child.route_retrieve(query, k=k, rewrite=rewrite)
        return [
            Hit(
                text=item["leaf"].text,
                metadata=dict(item["leaf"].metadata),
                score=item.get("score"),
            )
            for item in routed["results"]
        ]

    def vector_retrieve(query: str, k: int) -> list[Hit]:
        rewritten = rewrite(query)
        retriever = vector_index.as_retriever(similarity_top_k=k)
        return _hits_from_nodes(retriever.retrieve(rewritten))

    def tree_retrieve(query: str, k: int) -> list[Hit]:
        retriever = tree_index.as_retriever(retriever_mode="select_leaf", child_branch_factor=8)
        return _hits_from_nodes(retriever.retrieve(query))[:k]

    def chroma_similarity(query: str, k: int) -> list[Hit]:
        rewritten = rewrite(query)
        return _hits_from_lc_docs(chroma_store.similarity_search(rewritten, k=k))

    def chroma_mmr(query: str, k: int) -> list[Hit]:
        rewritten = rewrite(query)
        return _hits_from_lc_docs(chroma_store.max_marginal_relevance_search(rewritten, k=k))

    return [
        Technique(
            "parent_child_router",
            "LlamaIndex parent-child vector index with feature/requirement routing",
            parent_child_retrieve,
        ),
        Technique(
            "llamaindex_vector",
            "LlamaIndex VectorStoreIndex over Header-1 sections, stored in Chroma",
            vector_retrieve,
            rewrites_query=True,
        ),
        Technique(
            "llamaindex_tree",
            "LlamaIndex TreeIndex select_leaf over Header-1 sections",
            tree_retrieve,
        ),
        Technique(
            "chroma_similarity",
            "LangChain Chroma cosine similarity over Header-1 sections",
            chroma_similarity,
            rewrites_query=True,
        ),
        Technique(
            "chroma_mmr",
            "LangChain Chroma maximal marginal relevance over Header-1 sections",
            chroma_mmr,
            rewrites_query=True,
        ),
    ]
