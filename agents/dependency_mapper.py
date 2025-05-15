# agents/dependency_mapper.py

from core.logger import setup_logger
from core.file_utils import read_json, write_json

logger = setup_logger("dependency_mapper")

def run():
    logger.info("🔗 Running Dependency Mapper...")

    enterprise_index = read_json("migration_assist/enterprise/enterprise_index.json")
    reference_mapping = read_json("migration_assist/reference/mappings/reference_mapping.json")

    custom_map = {}

    # From enterprise framework
    for path, metadata in enterprise_index.items():
        for cls in metadata.get("classes", []):
            fqcn = path.replace("/", ".").replace(".java", "")
            custom_map[fqcn] = {
                "replacement": fqcn,
                "source": "enterprise_framework",
                "confidence": 0.95
            }

    # From reference mappings
    for legacy_path, info in reference_mapping.items():
        summary = info.get("transformation_summary", "")
        if "class" in summary:
            for line in summary.splitlines():
                if "class" in line and "→" in line:
                    try:
                        legacy_cls, spring_cls = line.split("→")
                        custom_map[legacy_cls.strip()] = {
                            "replacement": spring_cls.strip(),
                            "source": "reference_mapping",
                            "confidence": 0.85
                        }
                    except Exception:
                        continue

    write_json("migration_assist/reference/custom_dependency_mapping.json", custom_map)
    logger.info(f"✅ Dependency mapping complete. {len(custom_map)} entries created.\n")
