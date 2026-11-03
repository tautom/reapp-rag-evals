"""Retrieval and generation evaluation.

Evaluation metrics: Precision@k, Recall@k, and F1@k. A query is
scored against relevant_FR_ids when that list is present, otherwise against
relevant_AC_ids.

Generation asks one model to answer from the retrieved text, then scores
groundedness and completeness with LLM-as-judge prompts.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

from openai import OpenAI

from redfin_rag.corpus import ROOT
from redfin_rag.techniques import Hit

QUERIES_PATH = ROOT / "evaluation_tc_queries.json"
FR_RE = re.compile(r"FR-\d+", re.I)
AC_RE = re.compile(r"AC-\d+\.\d+", re.I)


def load_queries(path: Path = QUERIES_PATH) -> list[dict]:
    return json.loads(path.read_text())


def gold_ids(query: dict) -> tuple[str, list[str]]:
    fr_ids = query.get("relevant_FR_ids") or []
    if fr_ids:
        return "FR", list(fr_ids)
    return "AC", list(query.get("relevant_AC_ids") or [])


def ids_from_hits(hits: list[Hit], kind: str) -> list[str]:
    """Collect gold-style ids in retrieval order, without duplicates."""
    pattern = FR_RE if kind == "FR" else AC_RE
    found: list[str] = []
    seen: set[str] = set()

    def add(value: str | None):
        if not value:
            return
        normalized = value.upper()
        if normalized not in seen:
            seen.add(normalized)
            found.append(normalized)

    for hit in hits:
        requirement_id = hit.metadata.get("requirement_id")
        if kind == "FR" and requirement_id:
            add(requirement_id)
            continue
        for match in pattern.findall(hit.text or ""):
            add(match)
        for key in ("Header 2", "Header 1"):
            for match in pattern.findall(str(hit.metadata.get(key) or "")):
                add(match)
    return found


def calculate_retrieval_metrics(retrieved_ids: list[str], relevant_ids: list[str], k: int = 3) -> dict:
    """Precision@k, Recall@k, and F1@k. """
    retrieved_set = set(retrieved_ids[:k])
    relevant_set = set(relevant_ids)
    true_positives = len(retrieved_set & relevant_set)
    precision = true_positives / k if k > 0 else 0
    recall = true_positives / len(relevant_set) if relevant_set else 0
    f1 = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0
    )
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_positives": true_positives,
        "retrieved_count": k,
        "relevant_count": len(relevant_set),
    }


def _parse_score(output: str) -> float:
    for line in output.splitlines():
        if line.strip().lower().startswith("score:"):
            raw = line.split(":", 1)[1].strip().split()[0]
            return float(raw) / 10.0
    match = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", output)
    if match:
        return float(match.group(1)) / 10.0
    return 0.5


def _judge(client: OpenAI, prompt: str) -> dict:
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        timeout=30,
    )
    output = response.choices[0].message.content or ""
    return {"score": _parse_score(output), "explanation": output}


def generate_answer(client: OpenAI, question: str, hits: list[Hit]) -> str:
    context = "\n\n".join(hit.text for hit in hits if hit.text)
    prompt = f"""Answer the question using only the context. If the context does not contain the answer, say so.

CONTEXT:
{context}

QUESTION:
{question}
"""
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        timeout=60,
    )
    return response.choices[0].message.content or ""


def evaluate_groundedness(client: OpenAI, answer: str, hits: list[Hit]) -> dict:
    context = "\n\n".join(hit.text for hit in hits if hit.text)
    prompt = f"""Evaluate if the ANSWER is fully supported by the CONTEXT. Check for hallucinations or unsupported claims.

CONTEXT:
{context}

ANSWER:
{answer}

Rate the groundedness from 0 to 10:

Provide:
1. Score (0-10)
2. Reasoning (one sentence)

Format:
Score: X
Reasoning: <explanation>"""
    try:
        judged = _judge(client, prompt)
    except Exception as exc:
        return {"score": 0.5, "verdict": "ERROR", "explanation": str(exc)}
    score = judged["score"]
    verdict = "GROUNDED" if score >= 0.7 else "PARTIAL" if score >= 0.4 else "HALLUCINATED"
    return {"score": score, "verdict": verdict, "explanation": judged["explanation"]}


def evaluate_completeness(client: OpenAI, question: str, answer: str, reference_answer: str | None) -> dict:
    if reference_answer:
        prompt = f"""Evaluate if the ANSWER fully addresses the QUESTION compared to the REFERENCE ANSWER.

QUESTION:
{question}

REFERENCE ANSWER:
{reference_answer}

GENERATED ANSWER:
{answer}

Rate the completeness from 0 to 10:

Provide:
1. Score (0-10)
2. Reasoning (one sentence)

Format:
Score: X
Reasoning: <explanation>"""
    else:
        prompt = f"""Evaluate if the ANSWER fully addresses the QUESTION.

QUESTION:
{question}

ANSWER:
{answer}

Rate the completeness from 0 to 10:

Provide:
1. Score (0-10)
2. Reasoning (one sentence)

Format:
Score: X
Reasoning: <explanation>"""
    try:
        judged = _judge(client, prompt)
    except Exception as exc:
        return {"score": 0.5, "verdict": "ERROR", "explanation": str(exc)}
    score = judged["score"]
    verdict = "COMPLETE" if score >= 0.7 else "PARTIAL" if score >= 0.4 else "INCOMPLETE"
    return {"score": score, "verdict": verdict, "explanation": judged["explanation"]}


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0
