# agents/fix_and_compile.py

from core.file_utils import (
    read_file, write_file, write_json, read_json
)
from core.logger import setup_logger
from core.llm_client import LLMClient
from core.llm_output_utils import clean_markdown_code
import os
import re

logger = setup_logger("fix_and_compile")

PROMPT_PATH = "prompts/fix_and_compile_prompt.txt"
CHUNK_PLAN_PATH = "output/chunk_plan.json"
CONTEXT_PATH = "output/context_cache.json"
FIX_LOG_PATH = "output/fix_log.json"
MIGRATED_DIR = os.getenv("MIGRATED_DIR", "output")

STUB_PACKAGE = "com.example.stub"
STUB_DIR = os.path.join(MIGRATED_DIR, "src/main/java/com/example/stub")

os.makedirs(STUB_DIR, exist_ok=True)

# ... (same is_semantically_incomplete and generate_shim as before)

def run():
    logger.info("🛠 Running Fix & Compile Agent with shim fallback...")

    client = LLMClient()
    prompt_template = read_file(PROMPT_PATH)
    chunk_plan = read_json(CHUNK_PLAN_PATH)
    context_cache = read_json(CONTEXT_PATH)
    fix_log = {}

    for file_path, chunks in chunk_plan.items():
        new_chunks = []
        needs_fix = any(chunk["type"] != "SAFE" for chunk in chunks)

        full_content = read_file(file_path)
        if not needs_fix and not is_semantically_incomplete(full_content):
            logger.info(f"✅ Skipping semantically clean file: {file_path}")
            continue

        missing_classes = extract_missing_references(full_content)
        for cls in missing_classes:
            shim_path = os.path.join(STUB_DIR, f"{cls}.java")
            if not os.path.exists(shim_path):
                shim_code = generate_shim(cls)
                write_file(shim_path, shim_code)
                logger.warning(f"⚠️ Shim created for unresolved class: {cls}")

        for chunk in chunks:
            legacy_candidates = [
                ctx["content"] for path, ctx in context_cache.items()
                if ctx["source"] == "legacy" and path.endswith(file_path.split("/")[-1])
            ]
            legacy_code = legacy_candidates[0] if legacy_candidates else ""

            prompt = prompt_template + f"\n\nLegacy code:\n{legacy_code[:6000]}\n\nMigrated chunk:\n{chunk['content']}"
            messages = [
                {"role": "system", "content": "You're fixing partially migrated Java code."},
                {"role": "user", "content": prompt}
            ]

            try:
                response = client.chat(messages)
                cleaned = clean_markdown_code(response)
                new_chunks.append(cleaned)
                fix_log[file_path] = fix_log.get(file_path, []) + [{
                    "original": chunk["content"][:100],
                    "fixed": cleaned[:100],
                    "status": "success"
                }]
            except Exception as e:
                logger.warning(f"❌ Fix failed for {file_path}: {e}")
                fix_log[file_path] = fix_log.get(file_path, []) + [{
                    "original": chunk["content"][:100],
                    "fixed": "",
                    "status": f"error: {e}"
                }]
                new_chunks.append(chunk["content"])

        fixed_code = "\n\n".join(new_chunks)
        write_file(file_path, fixed_code)

    write_json(FIX_LOG_PATH, fix_log)
    logger.info("✅ Fixing complete. Code updated, shims created, and fix logs written.\n")
