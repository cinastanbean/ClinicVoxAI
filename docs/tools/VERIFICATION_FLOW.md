# Verification Flow (Existing Patient)

## Summary
When the intent requires PHI access (reports, modify appointments), verification is required.

## Steps
1. Router classifies intent as report/reschedule/cancel.
2. Supervisor allows proceed if confidence is sufficient.
3. Task Agent checks verification_status.
4. If unverified, ask for DOB or last visit ID.
5. Verification tool attempts match.
6. If match -> verification_status = verified.
7. If failure -> retry once, then handoff.

