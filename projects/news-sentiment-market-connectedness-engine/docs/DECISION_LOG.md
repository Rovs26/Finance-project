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
