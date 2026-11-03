#RAG and Evaluations. 

Compare indexing and retrieval techniques over a functional-requirements spec for a real estate website, then run evaluations to score each one on the same query set.

The spec is split two ways:

- Header-1 feature sections feed the vector index, the tree index, and Chroma.
- Header-1 parents and Header-2 leaves feed the parent-child index. Search runs on the leaves.

## Techniques

| Name | What it does |
|---|---|
| `parent_child_router` | LlamaIndex vector index over requirement leaves, with routing for "all requirements for a feature" versus one requirement |
| `llamaindex_vector` | LlamaIndex vector index over feature sections, stored in Chroma |
| `llamaindex_tree` | LlamaIndex tree index (`select_leaf`) over feature sections |
| `chroma_similarity` | LangChain Chroma cosine similarity over feature sections |
| `chroma_mmr` | LangChain Chroma maximal marginal relevance over feature sections |

Retrieval is scored with precision, recall, and F1 at `k` (default 3). Queries with `relevant_FR_ids` are scored on functional-requirement ids. Queries with only `relevant_AC_ids` are scored on acceptance-criteria ids. Unless `--skip-generation` is set, each technique also answers from the retrieved text and is scored for groundedness and completeness.

## Layout

```
parent/
  redfin_rag/                  # this repository
  redfin_specs.md              # source document
  evaluation_tc_queries.json   # questions and gold ids
  .env                         # API keys
```

An existing Chroma or tree index there is reused. The parent-child index is built in memory on each run.

## Setup

Python 3.12 or newer.

```bash
uv pip install llama-index llama-index-embeddings-openai llama-index-llms-openai \
  llama-index-vector-stores-chroma chromadb langchain-openai langchain-chroma \
  langchain-text-splitters langchain-core python-dotenv openai
```

Create `.env` in the parent directory:

```env
OPENAI_API_KEY=sk-your-key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4o-mini
```

`OPENAI_API_KEY` is required. The model names are optional.

## Run

From the parent directory, using the environment where those packages are installed:

```bash
uv run --no-project --python /path/to/venv/bin/python -m redfin_rag
```

If that environment is already active:

```bash
uv run --no-project -m redfin_rag
```

Retrieval only:

```bash
uv run --no-project --python /path/to/venv/bin/python -m redfin_rag --skip-generation
```

A subset of techniques, a different cutoff, or a different report path:

```bash
uv run --no-project --python /path/to/venv/bin/python -m redfin_rag \
  --techniques parent_child_router llamaindex_vector \
  --k 3 \
  --report evaluation_report.json
```

The run prints a comparison table and writes the per-query scores to the report file.
