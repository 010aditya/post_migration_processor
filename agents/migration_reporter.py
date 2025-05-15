# agents/migration_reporter.py

from core.logger import setup_logger
from core.file_utils import read_json, write_json

logger = setup_logger("migration_reporter")

def run():
    logger.info("📋 Generating Final Migration Report...")

    report = {}

    report["build_status"] = read_json("migration_assist/output/build_status.json")
    report["fix_log"] = read_json("migration_assist/output/fix_log.json")
    report["custom_dependency_mapping"] = read_json("migration_assist/reference/custom_dependency_mapping.json")
    report["chunk_plan"] = read_json("migration_assist/output/chunk_plan.json")
    report["enterprise_index"] = read_json("migration_assist/enterprise/enterprise_index.json")

    # Highlight unresolved files (with chunks marked NEEDS_CHUNKING)
    unresolved = []
    for path, chunks in report["chunk_plan"].items():
        for chunk in chunks:
            if chunk["type"] != "SAFE":
                unresolved.append(path)
                break

    report["manual_review_flags"] = list(set(unresolved))

    write_json("migration_assist/output/final_migration_report.json", report)
    logger.info("✅ Final report generated: output/final_migration_report.json\n")
