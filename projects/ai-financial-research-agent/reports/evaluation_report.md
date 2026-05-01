# Retrieval and Grounding Evaluation Report

## Scope

Phase 1 evaluates the local TF-IDF retrieval and template-based memo workflow. The checks are intentionally simple and transparent.

## Retrieval Coverage Results

- Research questions evaluated: 6
- Questions with retrieved evidence: 6
- Status: pass

Every Phase 1 research question returned five evidence rows.

## Source Traceability Results

- Evidence rows evaluated: 30
- Rows with citation, document ID, title, chunk ID, and snippet: 30
- Status: pass

Each retrieved evidence row can be traced back to a source document and chunk.

## Grounding Check Results

- Memo sections evaluated: 8
- Sections with citations found in the evidence table: 8
- Status: pass

The grounding check confirms that memo citations exist in the cited evidence table. It does not prove that every sentence is semantically complete or suitable for final research publication.

## Risk Flag Extraction Method

Risk flags use keyword rules across these categories:

- credit risk
- liquidity risk
- interest-rate risk
- inflation risk
- market risk
- operational risk
- profitability risk
- adoption risk

All eight categories were found in the retrieved evidence set.

## Limitations

- Synthetic sample documents only.
- TF-IDF retrieval can miss semantically related evidence.
- Keyword-based risk flags can over-tag or under-tag risk themes.
- Citation checks validate traceability, not full factual truth.
- No external LLM or paid API is used.

## Next Improvements

- Add a small human-labeled evaluation set.
- Add relevance thresholds by question.
- Add semantic retrieval or embeddings later.
- Add stricter claim-level citation validation before LLM drafting.
