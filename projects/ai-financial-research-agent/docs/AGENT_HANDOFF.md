# Agent Handoff

## Final Project State

The AI Financial Research Agent project is complete through Phase 2. It is a local, reproducible portfolio project for finance document research, evidence retrieval, citation grounding, and risk flag extraction.

No paid API, OpenAI API, external LLM, dashboard, or production parser has been added.

## Pipeline Built

- Local sample document ingestion from `data/sample_docs/`
- Document metadata export
- Text cleaning and chunking
- TF-IDF evidence retrieval
- Citation-style evidence table
- Template-based memo workflow
- Keyword-based risk flag extraction
- Retrieval coverage, source traceability, and grounding checks
- Portfolio-ready README and reports

## Key Outputs

- `reports/research_memo.md`
- `reports/prompt_notes.md`
- `reports/evaluation_report.md`
- `reports/resume_bullets.md`
- `reports/interview_talking_points.md`
- `reports/company_positioning.md`
- `reports/linkedin_post.md`
- `outputs/evidence/cited_evidence_table.csv`
- `outputs/evidence/risk_flags.csv`
- `outputs/retrieval/retrieval_evaluation_summary.csv`

## Evaluation Result

- Retrieval coverage: 6 of 6 research questions covered.
- Source traceability: 30 of 30 evidence rows traceable.
- Memo grounding: 8 of 8 memo sections grounded with citations found in the evidence table.
- Risk categories found: credit, liquidity, interest-rate, inflation, market, operational, profitability, and adoption risk.

## Reports Completed

- Research memo
- Prompt and workflow notes
- Evaluation report
- Resume bullets
- Interview talking points
- Company positioning
- LinkedIn post drafts

## Next Optional Improvements

- Add real public reports or user-provided documents.
- Add PDF and table parsing.
- Add semantic embeddings.
- Add optional LLM drafting with strict citation controls.
- Add API or dashboard for evidence review.
