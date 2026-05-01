# LinkedIn Post Drafts

## Short Post

I finished a portfolio project called AI Financial Research Agent.

It is a local Python workflow that ingests sample finance documents, chunks text, retrieves evidence with TF-IDF, flags risk themes, and builds a cited research memo.

No paid APIs or external LLMs are used. The goal was to practice traceable research workflows before adding more advanced tools.

## Medium Post

I finished a portfolio project: AI Financial Research Agent.

The project focuses on a practical problem in finance and risk research: how do you summarize documents while keeping the memo tied to evidence?

What it does:

- loads local sample finance documents
- chunks text into traceable segments
- retrieves relevant evidence with TF-IDF
- creates citation-style references for document chunks
- extracts keyword-based risk flags
- builds a template-based cited memo
- evaluates retrieval coverage, source traceability, and grounding

This is not a production research system, and the documents are synthetic portfolio examples. I intentionally kept Phase 1 local and reproducible without paid APIs so the retrieval and citation workflow is easy to inspect.

## Technical Post

Project completed: AI Financial Research Agent.

This is a local Python research workflow for finance document analysis. It uses:

- pandas for evidence tables
- scikit-learn TF-IDF for retrieval
- deterministic chunk IDs for traceability
- rule-based risk flags
- template-based memo sections with citations
- evaluation checks for coverage, traceability, and grounding

The key design choice was to avoid external LLMs in the first version. I wanted the evidence layer to work first: retrieve the right chunks, cite them clearly, and check whether memo sections can be traced back to source text.

Future improvements could include PDF parsing, semantic embeddings, a labeled evaluation set, and optional LLM drafting with strict citation guardrails.

This is a portfolio research prototype, not investment advice or a production-grade system.
