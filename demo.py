#!/usr/bin/env python3
"""Demo script showing how to use the LiteLLM provider with LangExtract."""

import os

import langextract as lx

# Create example data for few-shot learning
examples = [
    lx.data.ExampleData(
        text="John Smith is 30 years old and lives in New York.",
        extractions=[
            lx.data.Extraction(
                extraction_class="Person",
                extraction_text="John Smith",
                attributes={"age": "30", "location": "New York"},
            )
        ],
    )
]


def demo_litellm_provider():
    """Demonstrate the LiteLLM provider usage."""
    print("🚀 LangExtract LiteLLM Provider Demo")
    print("=" * 60)

    print("This demo shows how to use the LiteLLM provider with LangExtract.")
    print(
        "The provider supports a wide range of models through LiteLLM's unified API.\n"
    )

    print("📋 Supported Model Patterns:")
    patterns = [
        "litellm-* (explicit LiteLLM prefix)",
        "gpt-* (OpenAI models)",
        "claude-* (Anthropic models)",
        "gemini-*, palm-* (Google models)",
        "llama*, mistral*, codellama* (Meta/Mistral models)",
        "And many more open-source models",
    ]
    for pattern in patterns:
        print(f"  • {pattern}")

    print("\n📝 Usage Examples:")

    # Example 1: Using with litellm- prefix
    print("\n1. Using explicit LiteLLM prefix:")
    print("```python")
    print("result = lx.extract(")
    print(
        "    text_or_documents='Alice Johnson is 25 years old and works in San Francisco.',"
    )
    print("    model_id='litellm-gpt-3.5-turbo',")
    print(
        "    prompt_description='Extract person information including name, age, and location.',"
    )
    print("    examples=examples,")
    print("    api_key='your-openai-api-key'  # Or set OPENAI_API_KEY env var")
    print(")")
    print("```")

    # Example 2: Direct model ID
    print("\n2. Using direct model ID (auto-detected by pattern):")
    print("```python")
    print("result = lx.extract(")
    print("    text_or_documents='Bob Wilson is 35 years old and lives in Chicago.',")
    print("    model_id='gpt-4',")
    print(
        "    prompt_description='Extract person information including name, age, and location.',"
    )
    print("    examples=examples,")
    print("    api_key='your-openai-api-key'")
    print(")")
    print("```")

    # Example 3: Using other providers through LiteLLM
    print("\n3. Using other providers through LiteLLM:")
    print("```python")
    print("# Anthropic Claude")
    print(
        "result = lx.extract(..., model_id='claude-3-opus', api_key='your-anthropic-key')"
    )
    print("")
    print("# Google Gemini")
    print("result = lx.extract(..., model_id='gemini-pro', api_key='your-google-key')")
    print("")
    print("# Open source models via various providers")
    print(
        "result = lx.extract(..., model_id='llama-2-7b-chat', api_key='your-provider-key')"
    )
    print("```")

    print("\n🔧 Configuration Options:")
    config_options = [
        "api_key: API key for authentication",
        "api_base: Custom API base URL",
        "temperature: Sampling temperature (0.0-1.0)",
        "max_tokens: Maximum tokens to generate",
        "top_p: Top-p sampling parameter",
        "frequency_penalty: Frequency penalty (-2.0 to 2.0)",
        "presence_penalty: Presence penalty (-2.0 to 2.0)",
        "timeout: Request timeout in seconds",
    ]
    for option in config_options:
        print(f"  • {option}")

    print("\n🌟 Key Features:")
    features = [
        "✅ Unified API for 100+ models through LiteLLM",
        "✅ Automatic provider detection based on model ID patterns",
        "✅ Comprehensive error handling and logging",
        "✅ Support for all LiteLLM configuration options",
        "✅ Easy installation as a LangExtract plugin",
        "✅ Compatible with all LangExtract features",
    ]
    for feature in features:
        print(f"  {feature}")

    print("\n📦 Installation:")
    print("```bash")
    print("pip install langextract-litellm")
    print("```")

    print("\n🔑 Environment Variables:")
    env_vars = [
        "LITELLM_API_KEY: General LiteLLM API key",
        "OPENAI_API_KEY: OpenAI models",
        "ANTHROPIC_API_KEY: Anthropic Claude models",
        "GOOGLE_API_KEY: Google models",
        "And other provider-specific keys as supported by LiteLLM",
    ]
    for var in env_vars:
        print(f"  • {var}")

    print("\n" + "=" * 60)
    print("🎉 Provider successfully loaded and ready to use!")
    print("Set your API keys and start extracting structured data from text!")


if __name__ == "__main__":
    demo_litellm_provider()
