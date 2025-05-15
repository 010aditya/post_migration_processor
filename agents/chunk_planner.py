# agents/chunk_planner.py

from core.logger import setup_logger
from core.file_utils import list_files_by_extension, read_file, write_json
from core.config import MIGRATED_DIR, MAX_INPUT_TOKENS

logger = setup_logger("chunk_planner")

def run():
    logger.info("📐 Running Chunk Planner...")

    files = list_files_by_extension(MIGRATED_DIR)
    chunk_plan = {}

    for path in files:
        content = read_file(path)

        if len(content) < MAX_INPUT_TOKENS * 4:
            chunk_plan[path] = [{
                "type": "SAFE",
                "start": 0,
                "end": len(content),
                "content": content
            }]
            continue

        # Split by methods crudely (AST option is available for future)
        methods = content.split("public ")
        base = methods[0]
        chunks = []

        for idx, method in enumerate(methods[1:], start=1):
            chunk_code = "public " + method
            token_count = len(chunk_code) // 4
            label = "SAFE" if token_count < MAX_INPUT_TOKENS else "NEEDS_CHUNKING"

            chunks.append({
                "type": label,
                "content": chunk_code[:MAX_INPUT_TOKENS * 4]
            })

        chunk_plan[path] = chunks

    write_json("migration_assist/output/chunk_plan.json", chunk_plan)
    logger.info(f"✅ Chunk planning complete for {len(chunk_plan)} files.\n")
