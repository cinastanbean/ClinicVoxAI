# Parallel Merge Policy

## Goal
Resolve state updates when multiple agents run in a parallel branch.

## Current Policy
- Each branch runs on a cloned state.
- Top-level field diffs are compared.
- If two branches modify the same field with different values:
  - Record a conflict
  - Apply value from priority order: task > context

## Conflict Record
Stored in `state.meta.merge_conflicts` and in trace events as `merge_conflict`.
