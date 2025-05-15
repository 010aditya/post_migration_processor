# agents/build_fixer.py

import subprocess
import re
from core.logger import setup_logger
from core.file_utils import write_json, read_json

logger = setup_logger("build_fixer")

BUILD_LOG = "migration_assist/output/build_status.json"
FIX_LOG = "migration_assist/output/fix_log.json"

def run():
    logger.info("🔁 Running Build Fixer Agent...")

    success = False
    attempt = 0
    max_attempts = 3
    build_result = {}

    while attempt < max_attempts:
        logger.info(f"🔄 Attempt #{attempt + 1} to build project...")

        try:
            result = subprocess.run(
                ["./gradlew", "build", "--stacktrace"],
                cwd="output",
                capture_output=True,
                text=True,
                timeout=120
            )
            build_output = result.stdout + result.stderr
            if result.returncode == 0:
                logger.info("✅ Build succeeded.")
                success = True
                break

            logger.warning("❌ Build failed. Parsing errors...")
            build_result[f"attempt_{attempt + 1}"] = build_output[:5000]

            # Extract failing Java files from logs
            failing_files = set(re.findall(r'(?<=:compileJava).+?(/.+?\.java)', build_output))
            if not failing_files:
                logger.error("⚠️ No failing .java files found in build logs.")
                break

            for f in failing_files:
                logger.info(f"Triggering fix retry for: {f.strip()}")
                fix_log = read_json(FIX_LOG)
                fix_log[f] = fix_log.get(f, []) + [{"status": "retry_triggered"}]
                write_json(FIX_LOG, fix_log)

        except Exception as e:
            logger.error(f"❌ Build retry failed: {e}")
            break

        attempt += 1

    write_json(BUILD_LOG, {
        "build_passed": success,
        "retries": attempt,
        "last_log": build_result.get(f"attempt_{attempt}", "")[:2000]
    })

    if not success:
        logger.warning("❌ Final build attempt failed.")
    else:
        logger.info("🏁 Final build passed.")
