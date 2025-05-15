# Updated FixAndCompileAgent with stronger semantic validation for SAFE chunks

from core.file_utils import (
    read_file, write_file, write_json, read_json
)
from core.logger import setup_logger
from core.llm_client import LLMClient
import re

logger = setup_logger("fix_and_compile")

PROMPT_PATH = "migration_assist/prompts/fix_and_compile_prompt.txt"
CHUNK_PLAN_PATH = "migration_assist/output/chunk_plan.json"
CONTEXT_PATH = "migration_assist/output/context_cache.json"
FIX_LOG_PATH = "migration_assist/output/fix_log.json"

def is_semantically_incomplete(content: str) -> bool:
    # Heuristic 1: Contains TODOs
    if "TODO" in content:
        return True

    # Heuristic 2: Empty method bodies
    if re.search(r'public\s+[\w<>\[\]]+\s+\w+\s*\([^)]*\)\s*\{\s*\}', content):
        return True

    # Heuristic 3: Missing field injections
    if "@Autowired" not in content and "@Inject" not in content and "new " not in content:
        if re.search(r'(Service|Repository)', content):
            return True

    # Heuristic 4: Method call to undefined service field
    if re.search(r'(\w+)\.\w+\(', content):
        service_refs = re.findall(r'(\w+)\.\w+\(', content)
        for ref in service_refs:
            if not re.search(rf'(private|protected|public)\s+\w+\s+{ref}\s*;', content):
                return True

    # Heuristic 5: Unused imports (indicative of incomplete logic)
    if re.search(r'import\s+\w+\.(controller|service|dao|repository)\..*;', content) and not re.search(r'\w+\(', content):
        return True

    return False

def run():
    logger.info("\U0001f6e0 Running Fix & Compile Agent with semantic validation...")

    client = LLMClient()
    prompt_template = read_file(PROMPT_PATH)
    chunk_plan = read_json(CHUNK_PLAN_PATH)
    context_cache = read_json(CONTEXT_PATH)
    fix_log = {}

    for file_path, chunks in chunk_plan.items():
        new_chunks = []
        needs_fix = any(chunk["type"] != "SAFE" for chunk in chunks)

        if not needs_fix:
            full_content = read_file(file_path)
            if not is_semantically_incomplete(full_content):
                logger.info(f"✅ Skipping semantically clean file: {file_path}")
                continue  # really safe
            logger.info(f"⚠️ Forcing fix on semantically incomplete SAFE file: {file_path}")

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
