# LangExtract LiteLLM Provider

A provider plugin for LangExtract that supports 100+ LLM models through [LiteLLM](https://docs.litellm.ai/docs/#basic-usage)'s unified API, including OpenAI GPT models, Anthropic Claude, Google PaLM, Azure OpenAI, and many open-source models.

## Installation

```bash
pip install -e .
```

## Supported Models

This provider handles model IDs that start with `litellm` and supports a wide range of models through LiteLLM's unified API:

- **OpenAI models**: `litellm/gpt-4`, `litellm/gpt-4o`, `litellm/gpt-3.5-turbo`, etc.
- **Anthropic models**: `litellm/claude-3-opus`, `litellm/claude-3-sonnet`, `litellm/claude-3-haiku`, etc.
- **Google models**: `litellm/gemini-1.5-pro`, `litellm/palm-2`, etc.
- **Azure OpenAI**: `litellm/azure/your-deployment-name`
- **Open-source models**: `litellm/llama-2-7b-chat`, `litellm/mistral-7b`, `litellm/codellama-34b`, etc.
- **And many more**: See [LiteLLM's supported models](https://docs.litellm.ai/docs/providers)

**Note**: All model IDs must be prefixed with `litellm/` or `litellm-` to be handled by this provider.

## Environment Variables

Configure authentication using LiteLLM's standard environment variable format. Set the appropriate variables based on your provider:

### OpenAI
```bash
export OPENAI_API_KEY="your-api-key"
```

### Anthropic
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### HuggingFace
```bash
export HUGGINGFACE_API_KEY="your-api-key"
```

### Azure OpenAI
```bash
export AZURE_API_KEY="your-azure-key"
export AZURE_API_BASE="https://your-resource.openai.azure.com/"
export AZURE_API_VERSION="2024-02-01"
```

### Google (VertexAI)
```bash
export VERTEXAI_PROJECT="your-project-id"
export VERTEXAI_LOCATION="us-central1"
# Also run: gcloud auth application-default login
```

### Other Providers
See the [LiteLLM documentation](https://docs.litellm.ai/docs/#basic-usage) for environment variables for other providers like HuggingFace, Cohere, AI21, etc.

## Usage

### Basic Usage

```python
import langextract as lx

# Create model configuration
config = lx.factory.ModelConfig(
    model_id="litellm/azure/gpt-4o",  # or "gpt-4", "claude-3-sonnet", etc.
    provider="LiteLLMLanguageModel",
)
model = lx.factory.create_model(config)

# Extract entities
result = lx.extract(
    text_or_documents="Lady Juliet gazed longingly at the stars, her heart aching for Romeo",
    model=model,
    prompt_description="Extract characters, emotions, and relationships in order of appearance.",
    examples=[...]
)
```

### Complete Example with Examples

```python
import langextract as lx
import textwrap

# Define extraction prompt
prompt = textwrap.dedent("""\
    Extract characters, emotions, and relationships in order of appearance.
    Use exact text for extractions. Do not paraphrase or overlap entities.
    Provide meaningful attributes for each entity to add context.""")

# Provide high-quality examples to guide the model
examples = [
    lx.data.ExampleData(
        text="ROMEO. But soft! What light through yonder window breaks? It is the east, and Juliet is the sun.",
        extractions=[
            lx.data.Extraction(
                extraction_class="character",
                extraction_text="ROMEO",
                attributes={"emotional_state": "wonder"}
            ),
            lx.data.Extraction(
                extraction_class="emotion",
                extraction_text="But soft!",
                attributes={"feeling": "gentle awe"}
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="Juliet is the sun",
                attributes={"type": "metaphor"}
            ),
        ]
    )
]

# Create model configuration
config = lx.factory.ModelConfig(
    model_id="litellm/azure/gpt-4o",
    provider="LiteLLMLanguageModel",
)
model = lx.factory.create_model(config)

# Extract entities
result = lx.extract(
    text_or_documents="Lady Juliet gazed longingly at the stars, her heart aching for Romeo",
    model=model,
    prompt_description=prompt,
    examples=examples
)

print("✅ Extraction successful!")
print(f"Results: {result}")
```

### Model ID Formats

The model ID must start with `litellm/` or `litellm-` to be handled by this provider.

```python
# Explicit LiteLLM prefix
model_id = "litellm/azure/gpt-4o"
model_id = "litellm/gpt-4"
model_id = "litellm/claude-3-sonnet"

# Alternative prefix formats
model_id = "litellm-gpt-4o"
model_id = "litellm-claude-3-sonnet"
```

### Advanced Configuration

You can pass additional parameters supported by LiteLLM:

```python
config = lx.factory.ModelConfig(
    model_id="litellm/gpt-4",
    provider="LiteLLMLanguageModel",
    temperature=0.7,
    max_tokens=1000,
    top_p=0.9,
    frequency_penalty=0.1,
    presence_penalty=0.1,
    timeout=30,
)
```

## Expected Output

The extraction will return structured data with precise character intervals:

```python
AnnotatedDocument(
    extractions=[
        Extraction(
            extraction_class='character',
            extraction_text='Lady Juliet',
            char_interval=CharInterval(start_pos=0, end_pos=11),
            alignment_status=<AlignmentStatus.MATCH_EXACT: 'match_exact'>,
            attributes={'emotional_state': 'longing'}
        ),
        Extraction(
            extraction_class='emotion',
            extraction_text='aching',
            char_interval=CharInterval(start_pos=52, end_pos=58),
            alignment_status=<AlignmentStatus.MATCH_FUZZY: 'match_fuzzy'>,
            attributes={'feeling': 'heartfelt yearning'}
        ),
        Extraction(
            extraction_class='relationship',
            extraction_text='her heart aching for Romeo',
            char_interval=CharInterval(start_pos=42, end_pos=68),
            alignment_status=<AlignmentStatus.MATCH_EXACT: 'match_exact'>,
            attributes={'type': 'romantic longing'}
        )
    ],
    text='Lady Juliet gazed longingly at the stars, her heart aching for Romeo'
)
```

## Error Handling

The provider includes robust error handling and will return error messages instead of raising exceptions:

```python
# If API call fails, you'll get:
ScoredOutput(score=0.0, output="LiteLLM API error: [error details]")
```

## Development

1. Install in development mode: `pip install -e .`
2. Run tests: `python test_plugin.py`
3. Build package: `python -m build`
4. Publish to PyPI: `twine upload dist/*`

## Requirements

- `langextract`
- `litellm`

## License

Apache License 2.0