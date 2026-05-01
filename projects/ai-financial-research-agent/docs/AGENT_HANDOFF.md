# Agent Handoff

## Current State

Phase 0 and Phase 1 are complete. The project now has local sample document ingestion, chunking, TF-IDF retrieval, citation-style evidence grounding, rule-based risk flags, a template-based research memo, and basic retrieval evaluation.

No paid API, OpenAI API, external LLM, production parser, or dashboard has been added.

## Files Changed in Phase 1

- `notebooks/02_memo_generation_and_evaluation.ipynb`
- `notebooks/02_memo_generation_and_evaluation_executed.ipynb`
- `src/retrieval.py`
- `src/evaluation.py`
- `src/visualization.py`
- `reports/research_memo.md`
- `reports/prompt_notes.md`
- `reports/evaluation_report.md`
- `README.md`
- `docs/PRODUCTION_PROGRESS.md`
- `docs/KNOWN_ISSUES.md`
- `docs/AGENT_HANDOFF.md`

## Outputs Created

- `outputs/evidence/cited_evidence_table.csv`
- `outputs/evidence/risk_flags.csv`
- `outputs/evidence/memo_section_evidence_map.csv`
- `outputs/retrieval/research_question_retrieval.csv`
- `outputs/retrieval/retrieval_evaluation_summary.csv`
- `outputs/retrieval/coverage_by_question.csv`
- `outputs/retrieval/source_traceability.csv`
- `outputs/retrieval/grounding_checks.csv`
- `reports/research_memo.md`

## Evaluation Result

- Retrieval coverage: 6 of 6 research questions covered.
- Source traceability: 30 of 30 retrieved evidence rows traceable.
- Memo grounding: 8 of 8 memo sections grounded with citations found in the evidence table.
- Risk categories found: credit risk, liquidity risk, interest-rate risk, inflation risk, market risk, operational risk, profitability risk, and adoption risk.

## Commands Run

- `python3 -m compileall src`
- `python3 -m jupyter nbconvert --to notebook --execute notebooks/02_memo_generation_and_evaluation.ipynb --output 02_memo_generation_and_evaluation_executed.ipynb`
- `git status --short`

## Next Recommended Task

Build Phase 2 by polishing the GitHub README, final reports, resume bullets, interview talking points, company positioning, and LinkedIn post while keeping the local-only limitations clear.
