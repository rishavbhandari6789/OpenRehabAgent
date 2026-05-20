# Contributing

Thank you for your interest in OpenRehabAgent.

## Contribution areas

- pose-estimation adapters
- pain-localisation heuristics
- safety rules
- evaluation metrics
- documentation
- tests
- API examples

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Pull request guidelines

1. Keep clinical limitations clear.
2. Do not add medical claims.
3. Add tests for new logic.
4. Update documentation when behaviour changes.
5. Keep explanations transparent and reproducible.
