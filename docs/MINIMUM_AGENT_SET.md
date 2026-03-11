# Minimum Agent Set (Learning-Oriented)

## Goal
Learn multi-agent collaboration with a minimal but realistic structure.

## Recommendation
Use three agents initially:
1. Router Agent
2. Task Agent
3. Supervisor/Guard Agent

## Why Not More?
- Reduces state collisions
- Avoids fragile handoffs
- Keeps latency low

## When to Split Agents
Split into Registration, Verification, Scheduling, Report agents only after:
- Router accuracy >= 90%
- Task success >= 80%
- Latency <= 2s

