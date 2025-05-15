# agents/swagger_generator.py

from core.logger import setup_logger
from core.file_utils import list_files_by_extension, read_file, write_file
import re

logger = setup_logger("swagger_generator")

def run():
    logger.info("📘 Running Swagger Generator Agent...")

    controller_files = list_files_by_extension("output", extensions=(".java",))
    updated_count = 0

    for path in controller_files:
        content = read_file(path)
        if "@RestController" not in content:
            continue
        if "@Operation" in content:
            continue  # Already annotated

        content = re.sub(
            r"(public\s+[^\(]+\([^\)]*\)\s*\{)",
            r"@Operation(summary = \"TODO: add summary\")\n\1",
            content
        )
        write_file(path, content)
        updated_count += 1

    logger.info(f"✅ Swagger annotations added to {updated_count} controllers.")
