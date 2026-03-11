# LLM Router Contract

## Input
```json
{"text":"string"}
```

## Output
```json
{
  "patient_type": "new|existing|unknown",
  "intent": "registration|schedule|reschedule|cancel|report|insurance|medication|other|unknown",
  "confidence": 0.0
}
```

## Fallback Rule
If JSON is invalid or confidence < 0.4, fall back to RuleBasedRouter.
