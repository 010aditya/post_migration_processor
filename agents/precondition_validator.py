# agents/precondition_validator.py

import os
from core.logger import setup_logger
from core.file_utils import write_file

logger = setup_logger("precondition_validator")

def run():
    logger.info("🔍 Running Precondition Validator...")

    # 1. Gradle wrapper script (stub)
    if not os.path.exists("output/gradlew"):
        write_file("output/gradlew", "#!/bin/bash\n./gradlew build")
        logger.warning("Gradle wrapper script created as placeholder.")

    # 2. Spring Boot Main Class
    main_class_path = "output/src/main/java/com/example/MainApplication.java"
    if not os.path.exists(main_class_path):
        main_code = (
            "package com.example;\n\n"
            "import org.springframework.boot.SpringApplication;\n"
            "import org.springframework.boot.autoconfigure.SpringBootApplication;\n\n"
            "@SpringBootApplication\n"
            "public class MainApplication {\n"
            "    public static void main(String[] args) {\n"
            "        SpringApplication.run(MainApplication.class, args);\n"
            "    }\
