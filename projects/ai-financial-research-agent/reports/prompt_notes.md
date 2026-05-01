# Prompt and Generation Notes

## Why No Paid API Is Used

Phase 1 stays fully local so the project is reproducible from a fresh clone without paid API keys, external LLM services, or private data access. This keeps the first version focused on evidence retrieval, traceability, and evaluation.

## Template-Based Generation Approach

The research memo is generated with deterministic section templates. Each section is linked to a research question, retrieves top TF-IDF evidence chunks, and inserts citation-style references from the evidence table.

This is not an LLM-generated memo. It is closer to a structured analyst draft created from local retrieval results.

## Citation Handling

Citations use chunk-level labels such as `[FINLEN-CHUNK001]`. Each label maps back to:

- research question
- document ID
- document title
- chunk ID
- evidence snippet
- retrieval score

The mapping is saved in `outputs/evidence/cited_evidence_table.csv` and `outputs/evidence/memo_section_evidence_map.csv`.

## Source-Grounding Guardrails

- Memo sections must include citations.
- Citations must exist in the evidence table.
- Evidence rows must include document and chunk identifiers.
- Risk flags are keyword-based and should be reviewed by a person before formal use.

## Future LLM Improvement Path

A later version could add local or paid LLM drafting only after the retrieval layer is stronger. The preferred path would be:

1. Retrieve evidence.
2. Pass only cited evidence into a memo-drafting prompt.
3. Require citations in every generated claim.
4. Reject unsupported claims.
5. Keep the final memo editable and reviewable by a human analyst.
