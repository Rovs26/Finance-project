# Decision Log

## Use Local Sample Documents First

Phase 0 uses local synthetic sample documents so the pipeline is reproducible and does not depend on external data access. The documents are clearly labeled as portfolio examples.

## Use TF-IDF Before Embeddings

TF-IDF retrieval is transparent, local, and enough for a first retrieval prototype. Embeddings can be added later after the traceable baseline works.

## No Paid APIs in Phase 0

Phase 0 does not call paid APIs or the OpenAI API. The focus is ingestion, chunking, and retrieval infrastructure.

## Notebook-First Workflow

The first implementation is notebook-driven for clarity, with reusable code kept in `src/`.

## Stop at GitHub-Ready Portfolio Version

Phase 2 finalizes the project as a readable portfolio prototype instead of expanding into a larger product. Optional extensions such as API serving, dashboard review, real document ingestion, and embeddings are left for future work.

## Keep No-API Design as an Intentional Choice

The final version keeps the workflow local and reproducible. This makes the project easier to review because it does not require API keys, usage credits, or external services.

## Keep TF-IDF as the Transparent MVP Retrieval Method

TF-IDF remains the retrieval baseline for the final version. It is not the most advanced approach, but it is easy to explain, inspect, and evaluate before adding embeddings or LLM drafting.
