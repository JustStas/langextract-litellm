"""Provider implementation for LiteLLM."""

import logging
import os
from collections.abc import Iterator, Sequence

import langextract as lx
import litellm
from langextract import data, exceptions, inference, schema
from langextract.providers import registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@lx.providers.registry.register(r"^litellm", priority=10)
class LiteLLMLanguageModel(lx.inference.BaseLanguageModel):
    """LangExtract provider for LiteLLM.

    This provider supports a wide range of models through LiteLLM's unified API,
    including OpenAI GPT models, Anthropic Claude, Google PaLM, and many open-source models.

    Supported model patterns:
    - litellm-* (explicit LiteLLM prefix)
    - gpt-* (OpenAI models)
    - claude-* (Anthropic models)
    - gemini-*, palm-* (Google models)
    - llama*, mistral*, codellama* (Meta/Mistral models)
    - And many more open-source models
    """

    def __init__(self, model_id: str, api_key: str = None, **kwargs):
        """Initialize the LiteLLM provider.

        Args:
            model_id: The model identifier (e.g., 'gpt-4', 'claude-3-opus', 'llama-2-7b-chat').
            api_key: API key for authentication. If not provided, LiteLLM will automatically
                    look for provider-specific environment variables (OPENAI_API_KEY,
                    ANTHROPIC_API_KEY, GOOGLE_API_KEY, etc.)
            **kwargs: Any parameters supported by litellm.completion(), including:
                    - api_base: Custom API base URL
                    - temperature: Sampling temperature (0.0-1.0)
                    - max_tokens: Maximum tokens to generate
                    - top_p: Top-p sampling parameter
                    - frequency_penalty: Frequency penalty (-2.0 to 2.0)
                    - presence_penalty: Presence penalty (-2.0 to 2.0)
                    - timeout: Request timeout in seconds
                    - And any other LiteLLM-supported parameters
        """
        super().__init__()

        # Remove litellm prefix for actual model calls
        if model_id.startswith("litellm/"):
            self.model_id = model_id[8:]  # Remove 'litellm/' prefix
        elif model_id.startswith("litellm-"):
            self.model_id = model_id[8:]  # Remove 'litellm-' prefix
        else:
            self.model_id = model_id

        self.original_model_id = model_id

        # Store provider-specific parameters
        self.provider_kwargs = kwargs

        logger.info(f"Initialized LiteLLM provider for model: {self.model_id}")

    def infer(
        self, batch_prompts, **kwargs
    ) -> Iterator[Sequence[inference.ScoredOutput]]:
        """Run inference on a batch of prompts.

        Args:
            batch_prompts: List of prompts to process.
            **kwargs: Additional inference parameters that override instance defaults.

        Yields:
            Lists of ScoredOutput objects, one per prompt.
        """
        # Merge provider kwargs with call-time kwargs (call-time takes precedence)
        # api_params = {**self.provider_kwargs, **kwargs}

        for prompt in batch_prompts:
            try:
                logger.info(f"Calling LiteLLM completion for model {self.model_id}")

                # Format prompt as messages for chat models
                messages = [{"role": "user", "content": str(prompt)}]

                response = litellm.completion(
                    model=self.model_id,
                    messages=messages,
                    **self.provider_kwargs,
                )

                # Extract the response content
                if response.choices and len(response.choices) > 0:
                    content = response.choices[0].message.content
                    if content:
                        yield [lx.inference.ScoredOutput(score=1.0, output=content)]
                    else:
                        logger.warning(
                            f"Empty response from LiteLLM for model {self.model_id}"
                        )
                        yield [lx.inference.ScoredOutput(score=0.0, output="")]
                else:
                    logger.error(
                        f"No choices in response from LiteLLM for model {self.model_id}"
                    )
                    yield [lx.inference.ScoredOutput(score=0.0, output="")]

            except Exception as e:
                logger.error(
                    f"Error calling LiteLLM completion for model {self.model_id}: {str(e)}"
                )
                # Return an error output instead of raising
                error_msg = f"LiteLLM API error: {str(e)}"
                yield [lx.inference.ScoredOutput(score=0.0, output=error_msg)]
