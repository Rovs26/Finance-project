# Decision Log

## Use Local Sample Documents First

Phase 0 uses local synthetic sample documents so the pipeline is reproducible and does not depend on external data access. The documents are clearly labeled as portfolio examples.

## Use TF-IDF Before Embeddings

TF-IDF retrieval is transparent, local, and enough for a first retrieval prototype. Embeddings can be added later after the traceable baseline works.

## No Paid APIs in Phase 0

Phase 0 does not call paid APIs or the OpenAI API. The focus is ingestion, chunking, and retrieval infrastructure.

## Notebook-First Workflow

The first implementation is notebook-driven for clarity, with reusable code kept in `src/`.
