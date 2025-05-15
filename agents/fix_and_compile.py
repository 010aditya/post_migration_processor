# agents/fix_and_compile.py

from core.file_utils import (
    read_file, write_file, write_json, read_json
)
from core.logger import setup_logger
from core.llm_client import LLMClient

logger = setup_logger("fix_and_compile")

PROMPT_PATH = "migration_assist/prompts/fix_and_compile_prompt.txt"
CHUNK_PLAN_PATH = "migration_assist/output/chunk_plan.json"
CONTEXT_PATH = "migration_assist/output/context_cache.json"
FIX_LOG_PATH = "migration_assist/output/fix_log.json"

def run():
    logger.info("🛠 Running Fix & Compile Agent...")

    client = LLMClient()
    prompt_template = read_file(PROMPT_PATH)
    chunk_plan = read_json(CHUNK_PLAN_PATH)
    context_cache = read_json(CONTEXT_PATH)
    fix_log = {}

    for file_path, chunks in chunk_plan.items():
        new_chunks = []
        for chunk in chunks:
            if chunk["type"] == "SAFE":
                new_chunks.append(chunk["content"])
                continue

            legacy_candidates = [
                ctx["content"]
                for path, ctx in context_cache.items()
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
                new_chunks.append(response)
                fix_log[file_path] = fix_log.get(file_path, []) + [{
                    "original": chunk["content"][:100],
                    "fixed": response[:100],
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
    logger.info("✅ Fixing complete. Code updated and fix logs written.\n")
