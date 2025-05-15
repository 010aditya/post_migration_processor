# agents/precondition_validator.py

import os
from core.logger import setup_logger
from core.file_utils import write_file
from core.config import MIGRATED_DIR

logger = setup_logger("precondition_validator")

def run():
    logger.info("🔍 Running Precondition Validator...")

    # 1. Gradle wrapper stub
    gradlew_path = os.path.join(MIGRATED_DIR, "gradlew")
    if not os.path.exists(gradlew_path):
        write_file(gradlew_path, "#!/bin/bash\n./gradlew build")
        logger.warning(f"⚙️ Gradle wrapper script created: {gradlew_path}")

    # 2. Spring Boot Main class
    main_class_path = os.path.join(MIGRATED_DIR, "src/main/java/com/example/MainApplication.java")
    if not os.path.exists(main_class_path):
        main_class_code = """\
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MainApplication {
    public static void main(String[] args) {
        SpringApplication.run(MainApplication.class, args);
    }
}
"""
        write_file(main_class_path, main_class_code)
        logger.warning(f"🧵 Main class scaffolded at: {main_class_path}")

    # 3. application.yaml
    yaml_path = os.path.join(MIGRATED_DIR, "src/main/resources/application.yaml")
    if not os.path.exists(yaml_path):
        default_yaml = """spring:
  application:
    name: migrated-app
"""
        write_file(yaml_path, default_yaml)
        logger.warning(f"📄 application.yaml created at: {yaml_path}")

    logger.info("✅ Precondition validation complete.\n")
