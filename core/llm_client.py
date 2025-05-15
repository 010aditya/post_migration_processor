# core/llm_client.py

import os
from openai import OpenAI, AzureOpenAI
from tenacity import retry, stop_after_attempt, wait_fixed
from core.config import LLM_PROVIDER, MAX_RETRIES, RETRY_WAIT_SECONDS
from core.logger import setup_logger

logger = setup_logger("llm_client")

class LLMClient:
    def __init__(self):
        self.provider = LLM_PROVIDER
        if self.provider == "azure":
            self.client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version="2024-02-15-preview",
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
            )
            self.model = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")
        else:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4o"

    @retry(stop=stop_after_attempt(MAX_RETRIES), wait=wait_fixed(RETRY_WAIT_SECONDS))
    def chat(self, messages, max_tokens=4000, temperature=0.2):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            content = response.choices[0].message.content.strip()
            logger.info(f"✅ LLM call successful (provider={self.provider}, model={self.model})")
            return content
        except Exception as e:
            logger.error(f"❌ LLM call failed (provider={self.provider}, model={self.model}): {e}")
            raise

