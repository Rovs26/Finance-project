# Interview Talking Points

## 1. What problem does this project solve?

It shows how a finance research workflow can keep memo conclusions tied to source evidence. The project ingests documents, chunks them, retrieves relevant text, adds citations, and checks whether memo sections are grounded.

## 2. Why did you use TF-IDF instead of embeddings?

TF-IDF is transparent, local, and easy to explain. I wanted a baseline that works without paid APIs before adding more advanced retrieval.

## 3. Why avoid paid APIs?

For a portfolio project, reproducibility matters. Anyone reviewing the repo can run the workflow without keys, credits, or external services.

## 4. How are citations handled?

Each retrieved chunk gets a compact citation label such as `[FINLEN-CHUNK001]`. The label maps back to a document ID, document title, chunk ID, snippet, and retrieval score.

## 5. What does grounding mean in this project?

Grounding means each memo section includes citations that exist in the evidence table. It is a traceability check, not a guarantee that the memo is production-ready.

## 6. How are risk flags extracted?

Risk flags use keyword rules for categories such as credit risk, liquidity risk, market risk, operational risk, and adoption risk. The method is simple but auditable.

## 7. What are the main limitations?

The documents are synthetic, retrieval is TF-IDF only, risk flags are keyword-based, and the memo is template-based. A human analyst still needs to review the output.

## 8. How would you improve this?

I would add real public documents, PDF parsing, a small labeled evaluation set, semantic embeddings, and optional LLM drafting with strict citation rules.

## 9. How is this relevant to fintech or banking?

The same structure can support complaint review, credit policy research, risk monitoring notes, market updates, due diligence summaries, or internal research workflows.

## 10. What did you learn from building it?

The retrieval layer matters before memo generation. A polished summary is less useful if the evidence cannot be traced, checked, and challenged.
