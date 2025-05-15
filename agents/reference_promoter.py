# agents/reference_promoter.py

import os
from core.llm_client import LLMClient
from core.file_utils import list_files_by_extension, read_file, write_json
from core.logger import setup_logger
from core.config import REFERENCE_DIR

logger = setup_logger("reference_promoter")

OUTPUT_PATH = "migration_assist/reference/mappings/reference_mapping.json"
PROMPT_PATH = "migration_assist/prompts/reference_pattern_extraction.txt"

def run():
    if not REFERENCE_DIR or not os.path.exists(REFERENCE_DIR):
        logger.warning("⏭️ Skipping: REFERENCE_DIR not set or doesn't exist.")
        write_json(OUTPUT_PATH, {})
        return

    logger.info("🔍 Running Reference Promoter Agent...")

    client = LLMClient()
    prompt_template = read_file(PROMPT_PATH)
    mappings = {}

    for project in os.listdir(REFERENCE_DIR):
        legacy_dir = os.path.join(REFERENCE_DIR, project, "legacy")
        migrated_dir = os.path.join(REFERENCE_DIR, project, "migrated")
        if not os.path.exists(legacy_dir) or not os.path.exists(migrated_dir):
            continue

        legacy_files = list_files_by_extension(legacy_dir)
        migrated_files = list_files_by_extension(migrated_dir)

        for legacy_path in legacy_files:
            filename = os.path.basename(legacy_path)
            match = [f for f in migrated_files if os.path.basename(f) == filename]
            if not match:
                continue

            migrated_path = match[0]
            legacy_code = read_file(legacy_path)
            migrated_code = read_file(migrated_path)

            messages = [
                {"role": "system", "content": prompt_template},
                {"role": "user", "content": f"Legacy code:\n{legacy_code[:4000]}\n\nMigrated code:\n{migrated_code[:4000]}"}
            ]

            try:
                response = client.chat(messages)
                mappings[legacy_path] = {
                    "migrated_path": migrated_path,
                    "transformation_summary": response
                }
            except Exception as e:
                logger.warning(f"❌ Mapping failed for {legacy_path}: {e}")

    write_json(OUTPUT_PATH, mappings)
    logger.info(f"✅ Reference mapping complete. {len(mappings)} patterns learned.\n")
