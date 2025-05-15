# core/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

# Model + token settings
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")
MAX_INPUT_TOKENS = int(os.getenv("MAX_INPUT_TOKENS", 10000))
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", 4000))
MAX_RETRIES = int(os.getenv("LLM_RETRY_LIMIT", 3))
RETRY_WAIT_SECONDS = int(os.getenv("LLM_RETRY_WAIT", 2))

# Project paths
LEGACY_DIR = os.getenv("LEGACY_DIR", "legacy")
MIGRATED_DIR = os.getenv("MIGRATED_DIR", "output")
REFERENCE_DIR = os.getenv("REFERENCE_DIR", "").strip()
ENTERPRISE_FRAMEWORK_DIR = os.getenv("ENTERPRISE_FRAMEWORK_DIR", "").strip()
MAPPING_FILE = os.getenv("MAPPING_FILE", "mapping.json")
