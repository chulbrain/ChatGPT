# Knowledge Graph Example

This repository contains a simple knowledge graph implementation in Python.

## Files

- `knowledge_graph.py` - minimal script to build and query a knowledge graph.
- `gemini_kg.py` - optional script to create a graph using the Gemini API.
- `sample_data.csv` - example data used by the script.

## Usage

Run the script to print all edges in the sample data:

```bash
python3 knowledge_graph.py
```

Find a connection between two nodes (limited to depth 3):

```bash
python3 knowledge_graph.py --path Alice Python
```

### Gemini-based graph generation

The `gemini_kg.py` script demonstrates how to use the Gemini 2.5 Pro API to
extract triples from a PDF, text file, or URL. Set the `GEMINI_API_KEY`
environment variable and ensure the `google-generativeai`, `requests`, and
`PyPDF2` packages are installed.

Extract triples from a text file and save them to `kg.csv`:

```bash
python3 gemini_kg.py --text notes.txt --output kg.csv
```
