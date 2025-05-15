# agents/datasource_extractor.py

import re
from core.logger import setup_logger
from core.file_utils import list_files_by_extension, read_file, write_file

logger = setup_logger("datasource_extractor")

def extract_jdbc_info(content: str):
    urls = re.findall(r'jdbc:\w+:[^\s"\'<>]+', content)
    return list(set(urls))

def run():
    logger.info("💾 Running Datasource Extractor Agent...")

    legacy_files = list_files_by_extension("legacy")
    reference_files = list_files_by_extension("reference_migrations")

    jdbc_urls = set()

    for path in legacy_files + reference_files:
        try:
            content = read_file(path)
            urls = extract_jdbc_info(content)
            jdbc_urls.update(urls)
        except Exception as e:
            logger.warning(f"Could not extract JDBC from {path}: {e}")

    lines = ["spring:\n  datasource:\n"]
    for i, url in enumerate(jdbc_urls):
        lines.append(f"    ds{i+1}:\n")
        lines.append(f"      url: {url}\n")
        lines.append(f"      username: <username>\n")
        lines.append(f"      password: <password>\n")
        lines.append(f"      driver-class-name: <driver>\n")

    yaml_output = "\n".join(lines)
    write_file("output/src/main/resources/application.yaml", yaml_output)

    logger.info(f"✅ application.yaml updated with {len(jdbc_urls)} datasources.\n")
