# AI Financial Research Agent

Local finance research workflow that ingests sample documents, retrieves evidence with TF-IDF, extracts risk flags, and builds a cited template-based research memo.

**Disclaimer:** This is a portfolio analytics project. The sample documents are synthetic examples created for learning and demonstration. The project does not use paid APIs, external LLMs, private company reports, investment advice, or production research infrastructure.

## Business Problem

Finance, fintech, risk, and consulting teams often need to review documents quickly while keeping conclusions traceable to source evidence. This project builds a local baseline workflow for document ingestion, evidence retrieval, citation grounding, and research memo preparation before adding heavier AI or paid API tools.

## Target Roles and Companies

Target roles include finance analytics analyst, research analyst, AI workflow analyst, fintech analytics analyst, risk analytics analyst, and data analyst.

Target companies include GCash, Maya, ING Hubs Philippines, PwC Philippines, KPMG Philippines, JPMorgan Chase, MSCI, UnionBank, BPI, and startups.

## Phase Plan

| Phase | Status | Description |
|---|---|---|
| Phase 0 | Complete | Setup, sample document ingestion, chunking, TF-IDF retrieval |
| Phase 1 | Complete | Template memo generation, risk flags, citation grounding, retrieval evaluation |
| Phase 2 | Next | GitHub polish and final reports |

## What the Project Does

- Loads local sample finance documents from `data/sample_docs/`.
- Cleans and chunks text into traceable document segments.
- Builds a local TF-IDF retrieval index.
- Retrieves evidence for finance research questions.
- Creates citation-style references such as `[FINLEN-CHUNK001]`.
- Extracts rule-based risk flags across credit, liquidity, rates, inflation, market, operational, profitability, and adoption risks.
- Builds a template-based research memo from retrieved evidence.
- Evaluates retrieval coverage, source traceability, and memo grounding.

## How to Run

```bash
cd projects/ai-financial-research-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 -m jupyter nbconvert --to notebook --execute notebooks/01_document_ingestion_and_retrieval.ipynb --output 01_document_ingestion_and_retrieval_executed.ipynb
python3 -m jupyter nbconvert --to notebook --execute notebooks/02_memo_generation_and_evaluation.ipynb --output 02_memo_generation_and_evaluation_executed.ipynb
```

## Generated Outputs

Phase 0:

- `data/processed/corpus_metadata.csv`
- `outputs/chunks/document_chunks.csv`
- `outputs/retrieval/sample_retrieval_results.csv`
- `outputs/evidence/evidence_table.csv`

Phase 1:

- `outputs/evidence/cited_evidence_table.csv`
- `outputs/evidence/risk_flags.csv`
- `outputs/evidence/memo_section_evidence_map.csv`
- `outputs/retrieval/research_question_retrieval.csv`
- `outputs/retrieval/retrieval_evaluation_summary.csv`
- `outputs/retrieval/coverage_by_question.csv`
- `outputs/retrieval/source_traceability.csv`
- `outputs/retrieval/grounding_checks.csv`
- `reports/research_memo.md`

Figures:

- `reports/figures/chunks_by_document.png`
- `reports/figures/top_terms_overall.png`
- `reports/figures/retrieval_score_distribution.png`
- `reports/figures/risk_flags_by_category.png`
- `reports/figures/evidence_count_by_question.png`
- `reports/figures/source_traceability_status.png`
- `reports/figures/grounding_check_summary.png`

Generated processed data and output CSVs are ignored by Git and can be regenerated from the notebooks.

## Phase 1 Evaluation Snapshot

- Retrieval coverage: 6 of 6 research questions covered.
- Source traceability: 30 of 30 evidence rows traceable to document and chunk IDs.
- Memo grounding: 8 of 8 memo sections contain citations found in the evidence table.
- Risk flags found: credit risk, liquidity risk, interest-rate risk, inflation risk, market risk, operational risk, profitability risk, and adoption risk.

## Limitations

- Synthetic sample documents only.
- TF-IDF retrieval only; no embeddings yet.
- Template-based memo only; no external LLM or OpenAI API calls.
- Risk flags use transparent keyword rules and need human review.
- Grounding checks validate citation presence, not full semantic correctness.
- No production PDF, spreadsheet, or table parser yet.
- No dashboard yet.
