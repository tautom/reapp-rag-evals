"""Run each indexing and retrieval technique, evaluate it, and write a report.

Usage, from the parent directory of this package:

    python -m redfin_rag
    python -m redfin_rag --techniques parent_child_router llamaindex_vector
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from openai import OpenAI as OpenAIClient

from redfin_rag.corpus import ROOT, load_corpus
from redfin_rag.evaluation import (
    calculate_retrieval_metrics,
    evaluate_completeness,
    evaluate_groundedness,
    generate_answer,
    gold_ids,
    ids_from_hits,
    load_queries,
    mean,
)
from redfin_rag.techniques import _RewriteCache, build_techniques

REPORT_PATH = ROOT / "evaluation_report.json"


def configure_models() -> None:
    load_dotenv(ROOT / ".env", override=True)
    os.environ.setdefault("HTTPX_TIMEOUT", "300")
    logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)
    Settings.embed_model = OpenAIEmbedding(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        api_key=os.getenv("OPENAI_API_KEY"),
        timeout=120,
        max_retries=5,
    )
    Settings.llm = OpenAI(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
        timeout=300,
        max_retries=5,
        temperature=0.0,
    )


def evaluate_technique(technique, queries, k: int, client, skip_generation: bool) -> dict:
    retrieval_rows = []
    generation_rows = []
    print(f"\n{'=' * 80}\n{technique.name}\n{technique.description}\n{'=' * 80}")

    for index, item in enumerate(queries, 1):
        question = item["query"]
        kind, relevant = gold_ids(item)
        print(f"  [{index}/{len(queries)}] {item['query_id']} {question[:70]}")
        if not relevant:
            print("    skipped: no gold ids")
            continue
        try:
            hits = technique.retrieve(question, k)
        except Exception as exc:
            print(f"    retrieval error: {exc}")
            retrieval_rows.append(
                {
                    "query_id": item["query_id"],
                    "question": question,
                    "error": str(exc),
                }
            )
            continue

        retrieved = ids_from_hits(hits, kind)
        metrics = calculate_retrieval_metrics(retrieved, relevant, k=k)
        row = {
            "query_id": item["query_id"],
            "question": question,
            "id_kind": kind,
            "relevant": relevant,
            "retrieved": retrieved[:k],
            **metrics,
        }
        retrieval_rows.append(row)
        print(
            f"    P@{k}={metrics['precision']:.2f}  "
            f"R@{k}={metrics['recall']:.2f}  "
            f"F1@{k}={metrics['f1']:.2f}  "
            f"retrieved={retrieved[:k]}"
        )

        if skip_generation or not hits:
            continue
        try:
            answer = generate_answer(client, question, hits)
            groundedness = evaluate_groundedness(client, answer, hits)
            completeness = evaluate_completeness(
                client, question, answer, item.get("reference_answer")
            )
        except Exception as exc:
            print(f"    generation error: {exc}")
            continue
        generation_rows.append(
            {
                "query_id": item["query_id"],
                "question": question,
                "answer": answer,
                "groundedness_score": groundedness["score"],
                "groundedness_verdict": groundedness["verdict"],
                "completeness_score": completeness["score"],
                "completeness_verdict": completeness["verdict"],
            }
        )
        print(
            f"    groundedness={groundedness['score']:.2f} ({groundedness['verdict']})  "
            f"completeness={completeness['score']:.2f} ({completeness['verdict']})"
        )

    scored = [row for row in retrieval_rows if "precision" in row]
    summary = {
        "name": technique.name,
        "description": technique.description,
        "precision": mean([row["precision"] for row in scored]),
        "recall": mean([row["recall"] for row in scored]),
        "f1": mean([row["f1"] for row in scored]),
        "groundedness": mean([row["groundedness_score"] for row in generation_rows]),
        "completeness": mean([row["completeness_score"] for row in generation_rows]),
        "retrieval": retrieval_rows,
        "generation": generation_rows,
    }
    print(
        f"  mean P@{k}={summary['precision']:.3f}  "
        f"R@{k}={summary['recall']:.3f}  F1@{k}={summary['f1']:.3f}"
    )
    if generation_rows:
        print(
            f"  mean groundedness={summary['groundedness']:.3f}  "
            f"completeness={summary['completeness']:.3f}"
        )
    return summary


def print_comparison(results: list[dict], k: int) -> None:
    print(f"\n{'=' * 80}\nCOMPARISON\n{'=' * 80}")
    header = f"{'technique':<24} {'P@'+str(k):>8} {'R@'+str(k):>8} {'F1@'+str(k):>8} {'ground':>8} {'complete':>8}"
    print(header)
    for result in results:
        print(
            f"{result['name']:<24} "
            f"{result['precision']:>8.3f} "
            f"{result['recall']:>8.3f} "
            f"{result['f1']:>8.3f} "
            f"{result['groundedness']:>8.3f} "
            f"{result['completeness']:>8.3f}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate Redfin RAG indexing and retrieval techniques")
    parser.add_argument("--k", type=int, default=3, help="Cutoff for precision/recall (default: 3)")
    parser.add_argument("--skip-generation", action="store_true", help="Score retrieval only")
    parser.add_argument(
        "--techniques",
        nargs="*",
        help="Subset of technique names to run. Default: all",
    )
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    args = parser.parse_args(argv)

    configure_models()
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set. Add it to .env in the parent directory of this package.", file=sys.stderr)
        return 1

    print("Loading specs and building indexes...")
    corpus = load_corpus()
    print(
        f"  feature sections: {len(corpus['feature_docs'])}  "
        f"parents: {len(corpus['parent_nodes'])}  "
        f"leaves: {len(corpus['leaf_nodes'])}"
    )
    techniques = build_techniques(corpus, rewrite=_RewriteCache())
    if args.techniques:
        selected = set(args.techniques)
        techniques = [item for item in techniques if item.name in selected]
        missing = selected - {item.name for item in techniques}
        if missing:
            print(f"Unknown techniques: {', '.join(sorted(missing))}", file=sys.stderr)
            return 1

    queries = load_queries()
    client = OpenAIClient()
    results = [
        evaluate_technique(technique, queries, args.k, client, args.skip_generation)
        for technique in techniques
    ]
    print_comparison(results, args.k)

    payload = {"k": args.k, "queries": len(queries), "techniques": results}
    args.report.write_text(json.dumps(payload, indent=2))
    print(f"\nWrote {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
