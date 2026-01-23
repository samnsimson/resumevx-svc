from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.nebius import NebiusProvider
from app.core.config import settings


class LLMModel:
    openai = OpenAIChatModel(
        settings.nebius_extraction_model,
        provider=NebiusProvider(api_key=settings.nebius_api_key),
    )

    extraction_model = OpenAIChatModel(
        settings.nebius_extraction_model,
        provider=NebiusProvider(api_key=settings.nebius_api_key),
    )

    rewrite_model = OpenAIChatModel(
        settings.nebius_rewrite_model,
        provider=NebiusProvider(api_key=settings.nebius_api_key),
    )
