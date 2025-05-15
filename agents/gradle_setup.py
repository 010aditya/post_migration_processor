# agents/gradle_setup.py

import os
from core.logger import setup_logger
from core.file_utils import write_file
from core.config import MIGRATED_DIR

logger = setup_logger("gradle_setup")

BUILD_FILE = os.path.join(MIGRATED_DIR, "build.gradle")

def run():
    logger.info("⚙️ Running Gradle Setup Agent...")

    if os.path.exists(BUILD_FILE):
        logger.info(f"🟡 Skipping: build.gradle already exists at {BUILD_FILE}")
        return

    required_blocks = {
        "plugins": [
            "id 'java'",
            "id 'org.springframework.boot' version '3.4.3'",
            "id 'io.spring.dependency-management' version '1.1.0'"
        ],
        "repositories": ["mavenCentral()"],
        "dependencies": [
            "implementation 'org.springframework.boot:spring-boot-starter-web'",
            "implementation 'org.springframework.boot:spring-boot-starter-data-jpa'",
            "implementation 'org.springframework.boot:spring-boot-starter-thymeleaf'",
            "implementation 'org.springframework.boot:spring-boot-starter-validation'",
            "implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.3.0'",
            "runtimeOnly 'com.h2database:h2'",
            "testImplementation 'org.springframework.boot:spring-boot-starter-test'"
        ]
    }

    gradle_lines = []

    for block, entries in required_blocks.items():
        gradle_lines.append(f"{block} {{")
        for entry in entries:
            gradle_lines.append(f"    {entry}")
        gradle_lines.append("}\n")

    gradle_content = "\n".join(gradle_lines)
    write_file(BUILD_FILE, gradle_content)

    logger.info(f"✅ build.gradle generated at: {BUILD_FILE}\n")
