# Router Backend Options

## Purpose
Allow RouterAgent to swap between rule-based and LLM-based classification.

## Current State
- RuleBasedRouter is default.
- LLMRouter is a stub for future integration.

## Extension Plan
- Implement LLMRouter using a provider client (OpenAI/Claude/etc.).
- Validate JSON schema and fallback to RuleBasedRouter on failure.
