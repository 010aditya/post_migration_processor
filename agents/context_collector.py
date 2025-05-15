# agents/context_collector.py

import os
from core.logger import setup_logger
from core.file_utils import (
    list_files_by_extension, read_file, write_json
)
from core.config import LEGACY_DIR, MIGRATED_DIR

logger = setup_logger("context_collector")

def run():
    logger.info("📦 Running Multi-Source Context Collector...")

    legacy_files = list_files_by_extension(LEGACY_DIR)
    migrated_files = list_files_by_extension(MIGRATED_DIR)

    context = {}

    for path in legacy_files:
        try:
            content = read_file(path)
            context[path] = {
                "source": "legacy",
                "content": content[:2000]
            }
        except Exception as e:
            logger.warning(f"❌ Failed to read legacy file {path}: {e}")

    for path in migrated_files:
        try:
            content = read_file(path)
            context[path] = {
                "source": "migrated",
                "content": content[:2000]
            }
        except Exception as e:
            logger.warning(f"❌ Failed to read migrated file {path}: {e}")

    write_json("migration_assist/output/context_cache.json", context)
    logger.info(f"✅ Context collection complete. {len(context)} files processed.\n")
