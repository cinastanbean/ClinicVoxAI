# Verification Handoff Policy

## Rule
If verification attempts >= max_verification_attempts, set handoff_reason to "verification_failed".

## Behavior
- Supervisor sees handoff_reason and routes to handoff response.
- This prevents repeated prompts and protects PHI.
