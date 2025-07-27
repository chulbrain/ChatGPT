"""Gemini 2.5 Pro Knowledge Graph builder.

This script demonstrates how to extract edges from PDF, text, or URL content
using Google's Gemini API. Due to environment limitations this code will not
run here without the required dependencies and network access.
"""

from __future__ import annotations

import argparse
import csv
import os
from typing import Iterable, Tuple


class KnowledgeGraph:
    def __init__(self) -> None:
        self.graph: dict[str, list[Tuple[str, str]]] = {}

    def add_edge(self, subject: str, relation: str, obj: str) -> None:
        self.graph.setdefault(subject, []).append((relation, obj))

    def get_relations(self, subject: str) -> list[Tuple[str, str]]:
        return self.graph.get(subject, [])

    def _bfs(self, start: str, end: str, max_depth: int) -> list[str] | None:
        from collections import deque

        queue = deque([(start, [start])])
        visited = {start}
        while queue:
            node, path = queue.popleft()
            if node == end:
                return path
            if len(path) > max_depth:
                continue
            for _, neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def find_path(self, start: str, end: str, max_depth: int = 3) -> list[str] | None:
        return self._bfs(start, end, max_depth)


# ---------------------------------------------------------------------------
# Text extraction helpers
# ---------------------------------------------------------------------------

def _load_text_from_pdf(path: str) -> str:
    try:
        import PyPDF2  # type: ignore
    except ImportError:
        raise RuntimeError("PyPDF2 is required to read PDF files")

    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def _load_text_from_url(url: str) -> str:
    try:
        import requests  # type: ignore
    except ImportError:
        raise RuntimeError("requests is required to fetch URLs")

    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text


def _load_text_from_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Gemini API interaction (placeholder)
# ---------------------------------------------------------------------------

def _extract_triples_with_gemini(text: str) -> Iterable[Tuple[str, str, str]]:
    """Use Gemini API to turn text into (subject, relation, object) triples."""
    try:
        import google.generativeai as genai  # type: ignore
    except ImportError:
        raise RuntimeError(
            "google-generativeai package is required to call Gemini API"
        )

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-pro")

    prompt = (
        "Extract knowledge graph triples from the following text.\n"
        "Return a CSV with columns: subject, relation, object."
    )
    response = model.generate_content(prompt + "\n" + text)
    output = response.text.strip()

    for row in csv.reader(output.splitlines()):
        if len(row) == 3:
            yield tuple(col.strip() for col in row)


# ---------------------------------------------------------------------------
# Builder logic
# ---------------------------------------------------------------------------

def build_graph(pdf: str | None, text: str | None, url: str | None) -> KnowledgeGraph:
    input_text = ""
    if pdf:
        input_text += _load_text_from_pdf(pdf)
    if text:
        input_text += _load_text_from_file(text)
    if url:
        input_text += _load_text_from_url(url)

    kg = KnowledgeGraph()
    for subj, rel, obj in _extract_triples_with_gemini(input_text):
        kg.add_edge(subj, rel, obj)
    return kg


# ---------------------------------------------------------------------------
# Command line interface
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Build a knowledge graph with Gemini")
    parser.add_argument("--pdf", help="PDF file to process")
    parser.add_argument("--text", help="text file to process")
    parser.add_argument("--url", help="URL to fetch and process")
    parser.add_argument("--output", default="kg.csv", help="CSV file to save edges")
    parser.add_argument("--path", nargs=2, metavar=("START", "END"), help="find path after building graph")
    args = parser.parse_args()

    if not any([args.pdf, args.text, args.url]):
        parser.print_help()
        return

    kg = build_graph(args.pdf, args.text, args.url)

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for subject, relations in kg.graph.items():
            for relation, obj in relations:
                writer.writerow([subject, relation, obj])

    if args.path:
        start, end = args.path
        path = kg.find_path(start, end)
        if path:
            print(" -> ".join(path))
        else:
            print(f"No path found from {start} to {end}")


if __name__ == "__main__":
    main()
