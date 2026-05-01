# Known Issues

## Final Project Limitations

- No blocking final issue found after Phase 2 checks.
- Sample documents are synthetic portfolio examples only.
- Retrieval uses TF-IDF only.
- Memo generation is template-based only.
- Risk flags use keyword rules and can over-tag or under-tag evidence.
- No paid API, OpenAI API, or external LLM is used.
- No production PDF, spreadsheet, or table parser is built.
- Grounding checks validate citation traceability, not full semantic truth.
- No dashboard or API layer is included.

## Practical Notes

- Processed files under `data/processed/` are ignored by Git and should be regenerated from notebooks after cloning.
- Output files under `outputs/` are ignored by Git and should be regenerated from notebooks after cloning.
- Figures are committed because they help reviewers understand the workflow quickly.
