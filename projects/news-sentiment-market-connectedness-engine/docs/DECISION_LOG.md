# Decision Log

## Reuse Existing Prototype

The project is designed to preserve the expected prototype scripts and raw files where available. Phase 0 audits the current state before changing pipeline logic.

## Keep Legacy Scripts in `legacy/`

Legacy scripts are isolated from new reusable modules. This keeps original prototype logic reviewable while allowing cleaner `src/` modules to grow in later phases.

## Notebook-First Audit Workflow

The first phase uses an audit notebook so schema, coverage, and pipeline interpretation are visible to reviewers.

## No Trading Performance Claims

The project is positioned as market research and analytics infrastructure. It does not claim trading profitability or provide trading advice.

## Complete in Three Compressed Phases

The project will stop at a GitHub-ready portfolio version after audit, core analysis, and polish phases.

## Add Safe Local OpenAI Scoring in Phase 1B

Phase 1B uses `OPENAI_API_KEY` and `OPENAI_MODEL` from local `.env` when available. The key is not printed, saved, or committed. The pipeline keeps a rule-based fallback so analysis remains reproducible when API access is unavailable.

## Keep Connectedness Fallback Transparent

The recovered dataset is too small for formal GFEVD, so Phase 1B continues to use absolute-correlation connectedness as a documented fallback.

## Finalize at GitHub-Ready Portfolio Version

Phase 2 stops the project at a clean portfolio version. Larger data collection, real GFEVD, dashboard work, and backtest validation are left as optional future phases.

## Record Credential Cleanup in Legacy Scripts

Recovered legacy scripts were sanitized so committed code uses environment-variable configuration instead of direct credential assignment.

## Keep `.env` Local and `.env.example` Safe

`.env` remains ignored by Git. `.env.example` contains placeholders only so another user can understand the configuration without exposing local credentials.

## Keep No-Trading-Advice Boundary

Signal labels are kept as research labels. The project does not claim trading performance, provide investment advice, or present a live recommendation system.
