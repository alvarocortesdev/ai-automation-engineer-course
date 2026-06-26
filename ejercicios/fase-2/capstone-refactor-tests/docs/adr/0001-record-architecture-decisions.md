<!--
ADR template (Nygard style). Copy this file to 0002-…, 0003-… for each decision.
Write ADRs in English (Track 0). An ADR records ONE decision: its context, the
options you weighed, what you chose, and the consequence. Format ref: adr.github.io

Write the ADRs you DOUBTED — the decision you almost made the other way is the
one worth documenting. "I extracted a pure core" is obvious; "I did NOT add a
Factory even though the tutorial said to, because there is a single product type"
is the one a reviewer wants to read.
-->

# ADR 0001 — Record architecture decisions

- **Status:** accepted
- **Date:** 2026-06-26

## Context
This project (the F2 capstone) makes design decisions that future-me will not
remember in six months. Without a written record, the *why* dies with the commit.

## Decision
We record every significant architectural decision as a Markdown ADR in
`docs/adr/`, numbered sequentially, using this template.

## Consequences
- **Positive:** decisions are reviewable, the reasoning survives, and the
  capstone satisfies DoD 1 (spec + ADRs).
- **Negative:** a small writing overhead per decision (acceptable — only
  *significant* decisions get an ADR, not every commit).

## Options considered
1. **No ADRs, comments only** — rejected: comments rot and scatter; no single
   place tells the design story.
2. **A single DECISIONS.md** — rejected: grows into an unsearchable wall of text.
3. **One file per decision (this ADR)** — chosen: greppable, diff-friendly,
   industry-standard.
