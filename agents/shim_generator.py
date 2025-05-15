# agents/shim_generator.py

import os
from core.logger import setup_logger
from core.file_utils import write_file

logger = setup_logger("shim_generator")

def generate_stub_class(fqcn: str) -> str:
    parts = fqcn.split(".")
    class_name = parts[-1]
    package = ".".join(parts[:-1])

    return f"""package {package};

public class {class_name} {{
    // [Migration Stub] This class was generated as a fallback.
}}
"""

def run(missing_classes: list):
    logger.info("🧱 Running Shim Generator Agent...")

    for fqcn in missing_classes:
        stub_code = generate_stub_class(fqcn)
        path = os.path.join("output", "migration-shims", *fqcn.split(".")) + ".java"
        write_file(path, stub_code)
        logger.info(f"🧩 Shim generated for: {fqcn}")

    logger.info("✅ All stubs created.\n")
