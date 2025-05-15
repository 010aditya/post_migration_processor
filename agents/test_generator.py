# agents/test_generator.py

import os
from core.logger import setup_logger
from core.file_utils import list_files_by_extension, read_file, write_file

logger = setup_logger("test_generator")

def generate_test_class(class_name, package_name):
    return f"""package {package_name};

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class {class_name}Test {{

    @Test
    public void dummyTest() {{
        assertTrue(true);
    }}
}}
"""

def run():
    logger.info("🧪 Running Test Generator Agent...")

    java_files = list_files_by_extension("output/src/main/java", extensions=(".java",))
    test_dir = "output/src/test/java"
    created = 0

    for path in java_files:
        if path.endswith("Test.java"):
            continue

        content = read_file(path)
        if "@RestController" not in content and "@Service" not in content:
            continue

        class_name = os.path.basename(path).replace(".java", "")
        package_parts = path.split("src/main/java/")[-1].split("/")[:-1]
        package_name = ".".join(package_parts)

        test_code = generate_test_class(class_name, package_name)
        test_path = os.path.join(test_dir, *package_parts, f"{class_name}Test.java")

        write_file(test_path, test_code)
        created += 1

    logger.info(f"✅ {created} JUnit test files generated.\n")
