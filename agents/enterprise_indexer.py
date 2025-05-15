# agents/enterprise_indexer.py

import os
import re
from core.file_utils import list_files_by_extension, read_file, write_json
from core.logger import setup_logger
from core.config import ENTERPRISE_FRAMEWORK_DIR

logger = setup_logger("enterprise_indexer")

def extract_java_signatures(content):
    class_match = re.findall(r"(public\s+)?(abstract\s+)?class\s+(\w+)", content)
    interface_match = re.findall(r"interface\s+(\w+)", content)
    annotation_match = re.findall(r"@\w+", content)
    return {
        "classes": [match[-1] for match in class_match],
        "interfaces": interface_match,
        "annotations": list(set(annotation_match))
    }

def run():
    if not ENTERPRISE_FRAMEWORK_DIR or not os.path.exists(ENTERPRISE_FRAMEWORK_DIR):
        logger.warning("⏭️ Skipping: ENTERPRISE_FRAMEWORK_DIR not set or doesn't exist.")
        write_json("migration_assist/enterprise/enterprise_index.json", {})
        return

    logger.info("🔍 Indexing Enterprise Framework...")

    index = {}
    java_files = list_files_by_extension(ENTERPRISE_FRAMEWORK_DIR)

    for path in java_files:
        try:
            content = read_file(path)
            sigs = extract_java_signatures(content)
            index[path] = sigs
        except Exception as e:
            logger.warning(f"❌ Failed to parse {path}: {e}")

    write_json("migration_assist/enterprise/enterprise_index.json", index)
    logger.info(f"✅ Indexed {len(index)} enterprise files.\n")
