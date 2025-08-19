        # LangExtract LiteLLM Provider

A provider plugin for LangExtract that supports LiteLLM models.

## Installation

```bash
pip install -e .
```

## Supported Model IDs

- `litellm*`: Models matching pattern ^litellm

## Environment Variables

- `LITELLM_API_KEY`: API key for authentication

## Usage

```python
import langextract as lx

result = lx.extract(
    text="Your document here",
    model_id="litellm-model",
    prompt_description="Extract entities",
    examples=[...]
)
```

## Development

1. Install in development mode: `pip install -e .`
2. Run tests: `python test_plugin.py`
3. Build package: `python -m build`
4. Publish to PyPI: `twine upload dist/*`

## License

Apache License 2.0
