# Prompt and Workflow Notes

## Local Template Workflow

Phase 1 uses deterministic templates rather than external text generation. Each memo section is tied to a research question, retrieves top TF-IDF evidence chunks, and inserts citation-style references from the evidence table.

The goal is to show the evidence workflow first: retrieve, cite, draft, and check grounding.

## Why No Paid APIs Are Used

The project is designed to run from a fresh clone without API keys, usage credits, or private data access. This keeps the first version easy to reproduce and easy to inspect during interviews.

## Source-Grounding Rules

- Every memo section should include at least one citation.
- Every citation must exist in `outputs/evidence/cited_evidence_table.csv`.
- Every cited evidence row must include a document ID, document title, chunk ID, snippet, and retrieval score.
- Risk flags are keyword-based and should be reviewed before formal use.

## Optional Future LLM Path

A later version could add LLM drafting after the retrieval and grounding layer is stronger. A safer flow would be:

1. Retrieve evidence locally.
2. Pass only cited evidence into the drafting step.
3. Require citations for material claims.
4. Reject or flag unsupported claims.
5. Keep a human analyst review step before final use.

LLM integration is intentionally outside the current version.
