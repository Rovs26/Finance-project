# Retrieval and Grounding Evaluation Report

## Scope

This report summarizes the Phase 1 checks for the local TF-IDF retrieval and template memo workflow.

## Retrieval Coverage

- Research questions evaluated: 6
- Questions with retrieved evidence: 6
- Result: pass

Every research question returned five evidence rows. This confirms that the local index can retrieve material for each planned memo section.

## Source Traceability

- Evidence rows evaluated: 30
- Rows with citation, document ID, title, chunk ID, and snippet: 30
- Result: pass

Each retrieved evidence row can be traced back to a specific document and chunk.

## Grounding Checks

- Memo sections evaluated: 8
- Sections with citations found in the evidence table: 8
- Result: pass

The check confirms citation consistency. It does not prove that every sentence is complete, final, or suitable for a real investment research report.

## Risk Flag Extraction

The workflow uses transparent keyword rules for:

- credit risk
- liquidity risk
- interest-rate risk
- inflation risk
- market risk
- operational risk
- profitability risk
- adoption risk

All eight categories appeared in the retrieved evidence set.

## Limitations

- Synthetic sample documents only.
- TF-IDF can miss semantic matches that use different wording.
- Keyword flags can create false positives.
- Citation checks validate traceability, not full factual truth.
- No external LLM, paid API, or production parser is used.

## Next Improvements

- Add a small hand-labeled relevance set.
- Add relevance thresholds by question.
- Add embeddings after keeping the citation workflow intact.
- Add claim-level support checks before any optional LLM drafting.
