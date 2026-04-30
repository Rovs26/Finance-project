# Decision Log

## Use Synthetic Bond Book First

The project starts with a synthetic bond book so the fixed income mechanics are clear and reproducible without implying access to confidential bank, insurer, or issuer-level holdings.

## Notebook-First Workflow

The first implementation is notebook-driven so the calculations, assumptions, and interpretation are easy to inspect. Reusable logic is still kept in `src/` modules.

## Stop Before Dashboard

The compressed scope stops at a GitHub-ready portfolio version before building any dashboard. The priority is the analytics foundation: cash flows, pricing, and documentation.

## Transparent Pricing Assumptions

Phase 0 uses fixed-rate bullet bonds, simple Actual/365 timing, and flat bond-level market yields. These assumptions keep the first version explainable before adding duration, convexity, or curve-based stress testing.
