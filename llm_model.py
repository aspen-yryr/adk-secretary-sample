from google.adk.models.lite_llm import LiteLlm

from config import config


def get_llm(disable_parallel_tool_calls: bool = False) -> LiteLlm:
    if disable_parallel_tool_calls:
        return LiteLlm(
            model="openai/gpt-4o-2024-08-06",
            api_key=config.api_key.get_secret_value(),
            parallel_tool_calls=False,
        )
    return LiteLlm(
        model="openai/gpt-4o-2024-08-06",
        api_key=config.api_key.get_secret_value(),
    )
