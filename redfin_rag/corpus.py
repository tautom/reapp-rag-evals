"""
Feature documents are split on Header 1 only. Those feed the vector index,
the tree index, and the LangChain Chroma store.

Parent-child leaves are split on Header 1 / Header 2 / Header 3. Retrieval
searches leaves; parents stay attached as feature context.
"""

from __future__ import annotations

import re
from collections import OrderedDict
from pathlib import Path

from langchain_core.documents import Document as LCDocument
from langchain_text_splitters import MarkdownHeaderTextSplitter
from llama_index.core import Document as LlamaDocument
from llama_index.core.schema import NodeRelationship, TextNode

ROOT = Path(__file__).resolve().parents[1]
SPECS_PATH = ROOT / "redfin_specs.md"


def _header1_id(header_1: str) -> str:
    header_1 = (header_1 or "").strip()
    match = re.search(r"^(\d+)\.", header_1)
    return match.group(1) if match else re.sub(r"\W+", "_", header_1)[:40]


def _feature_name(header_1: str) -> str:
    header_1 = (header_1 or "").strip()
    match = re.match(r"^\s*\d+\.\s*(.+)$", header_1)
    return match.group(1).strip() if match else header_1


def _split_header2(header_2: str) -> tuple[str, str]:
    """Split 'FR-020 — Search by Location' into ('FR-020', 'Search by Location')."""
    header_2 = re.sub(r"^#+\s*", "", (header_2 or "").strip())
    dashes = "-\u2010\u2011\u2012\u2013\u2014\u2015:"
    match = re.match(r"^(FR-\d+)\s*[" + dashes + r"]*\s*(.*)$", header_2)
    if match:
        return match.group(1), match.group(2).strip()
    match = re.search(r"(FR-\d+)", header_2)
    if match:
        rest = header_2[match.end() :].lstrip(" \t" + dashes)
        return match.group(1), rest.strip()
    return "", header_2


def _strip_markdown_headers(body: str) -> str:
    kept = []
    for line in (body or "").splitlines():
        if re.match(r"^#{1,6}\s+", line.strip()):
            continue
        kept.append(line)
    return "\n".join(kept).strip()


def _format_leaf_text(header_1: str, header_2: str, header_3: str, body: str) -> str:
    feature = _feature_name(header_1)
    req_id, req_name = _split_header2(header_2)
    ac = (header_3 or "").strip()
    body = _strip_markdown_headers(body)
    parts = [f"Feature: {feature}"]
    if req_id:
        parts.append(f"requirement_id: {req_id}")
    parts.append(f"Requirement: {req_name}")
    if ac:
        parts.append("Acceptance Criteria:")
    if body:
        parts.extend(["", body])
    return "\n".join(parts) + "\n"


def _clean_header_metadata(metadata: dict) -> dict:
    cleaned = {}
    for key, value in metadata.items():
        if isinstance(value, str):
            cleaned[key] = re.sub(r"^\s*\d+[\.\)]?\s*[\—-]?\s*", "", value).strip()
        else:
            cleaned[key] = value
    return cleaned


def load_feature_documents(specs_text: str) -> tuple[list[LlamaDocument], list[LCDocument]]:
    """Header-1 sections used by the vector, tree, and Chroma indexes."""
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "Header 1")])
    chunks = splitter.split_text(specs_text)
    llama_docs = []
    lc_docs = []
    for chunk in chunks:
        metadata = _clean_header_metadata(chunk.metadata)
        llama_docs.append(LlamaDocument(text=chunk.page_content, metadata=metadata))
        lc_docs.append(LCDocument(page_content=chunk.page_content, metadata=metadata))
    return llama_docs, lc_docs


def build_parent_child(specs_text: str) -> tuple[list[TextNode], list[TextNode], OrderedDict]:
    """Header-1 parents and Header-2 leaves they are linked together to provide a hierarchical context."""
    parent_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "Header 1")],
        strip_headers=True,
    )
    leaf_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")],
        strip_headers=True,
    )
    parent_sections = parent_splitter.split_text(specs_text)
    leaf_sections = leaf_splitter.split_text(specs_text)

    parent_nodes: list[TextNode] = []
    parent_by_id: OrderedDict[str, TextNode] = OrderedDict()
    for section in parent_sections:
        header_1 = (section.metadata.get("Header 1") or "").strip()
        if not header_1:
            continue
        parent_id = f"parent-{_header1_id(header_1)}"
        feature_id = _header1_id(header_1)
        feature_name = _feature_name(header_1)
        parent_node = TextNode(
            text=f"feature_id: {feature_id}\nFeature: {feature_name}\n",
            id_=parent_id,
            metadata={
                "node_type": "parent",
                "Header 1": header_1,
                "parent_id": parent_id,
                "feature_id": feature_id,
                "feature_name": feature_name,
            },
        )
        parent_nodes.append(parent_node)
        parent_by_id[parent_id] = parent_node

    leaf_nodes: list[TextNode] = []
    seen_ids: dict[str, int] = {}
    for section in leaf_sections:
        header_1 = (section.metadata.get("Header 1") or "").strip()
        header_2 = (section.metadata.get("Header 2") or "").strip()
        header_3 = (section.metadata.get("Header 3") or "").strip()
        if not header_2:
            continue
        parent_id = f"parent-{_header1_id(header_1)}"
        parent_node = parent_by_id.get(parent_id)
        if parent_node is None:
            continue

        req_id, req_name = _split_header2(header_2)
        leaf_text = _format_leaf_text(header_1, header_2, header_3, section.page_content)
        slug = req_id or re.sub(r"\W+", "-", header_2)[:48]
        base_id = f"leaf-{_header1_id(header_1)}-{slug}"
        seen_ids[base_id] = seen_ids.get(base_id, 0) + 1
        leaf_id = base_id if seen_ids[base_id] == 1 else f"{base_id}-{seen_ids[base_id]}"
        leaf_node = TextNode(
            text=leaf_text,
            id_=leaf_id,
            metadata={
                "node_type": "leaf",
                "Header 1": header_1,
                "Header 2": header_2,
                "Header 3": section.metadata.get("Header 3", "Acceptance Criteria"),
                "parent_id": parent_id,
                "feature_id": _header1_id(header_1),
                "feature_name": _feature_name(header_1),
                "requirement_id": req_id,
                "requirement_name": req_name,
            },
        )
        leaf_node.relationships[NodeRelationship.PARENT] = parent_node.as_related_node_info()
        child_list = list(parent_node.child_nodes or [])
        child_list.append(leaf_node.as_related_node_info())
        parent_node.relationships[NodeRelationship.CHILD] = child_list
        leaf_nodes.append(leaf_node)

    return parent_nodes, leaf_nodes, parent_by_id


def load_corpus(specs_path: Path = SPECS_PATH):
    specs_text = specs_path.read_text()
    feature_docs, lc_docs = load_feature_documents(specs_text)
    parent_nodes, leaf_nodes, parent_by_id = build_parent_child(specs_text)
    return {
        "feature_docs": feature_docs,
        "lc_docs": lc_docs,
        "parent_nodes": parent_nodes,
        "leaf_nodes": leaf_nodes,
        "parent_by_id": parent_by_id,
    }
