import os

folders = [
    "migration_assist/agents",
    "migration_assist/core",
    "migration_assist/orchestrator",
    "migration_assist/reference/embeddings",
    "migration_assist/reference/mappings",
    "migration_assist/enterprise",
    "migration_assist/output",
    "migration_assist/scripts"
]

files = {
    "migration_assist/agents": [
        "precondition_validator.py",
        "context_collector.py",
        "enterprise_indexer.py",
        "reference_promoter.py",
        "dependency_mapper.py",
        "chunk_planner.py",
        "fix_and_compile.py",
        "build_fixer.py",
        "gradle_setup.py",
        "swagger_generator.py",
        "test_generator.py",
        "shim_generator.py",
        "datasource_extractor.py",
        "migration_reporter.py",
        "__init__.py"
    ],
    "migration_assist/core": [
        "file_utils.py",
        "java_parser.py",
        "llm_client.py",
        "logger.py",
        "config.py",
        "__init__.py"
    ],
    "migration_assist/orchestrator": [
        "migration_coordinator.py",
        "__init__.py"
    ],
    "migration_assist/reference/embeddings": [
        "embedding_index.json"
    ],
    "migration_assist/reference/mappings": [
        "reference_mapping.json"
    ],
    "migration_assist/reference": [
        "custom_dependency_mapping.json"
    ],
    "migration_assist/enterprise": [
        "enterprise_index.json"
    ],
    "migration_assist/output": [
        "context_cache.json",
        "dependency_graph.json",
        "injection_map.json",
        "chunk_plan.json",
        "fix_log.json",
        "build_status.json",
        "final_migration_report.json",
        "datasource_summary.json",
        "manual_review_flags.json"
    ],
    "migration_assist/scripts": [
        "init.sh",
        "init.bat",
        "run_tool.py"
    ],
    "migration_assist": [
        "README.md",
        "requirements.txt",
        "setup.py"
    ]
}

# Create directories
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files with placeholders
for folder, file_list in files.items():
    for file in file_list:
        file_path = os.path.join(folder, file)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                if file.endswith(".py"):
                    f.write(f"# Placeholder for {file}\n")
                elif file.endswith(".json"):
                    f.write("{}\n")
                elif file.endswith(".sh") or file.endswith(".bat"):
                    f.write("# Placeholder script\n" if file.endswith(".sh") else ":: Placeholder script\n")
                else:
                    f.write(f"# {file} - Placeholder\n")

print("✅ Migration Assist folder structure and placeholders created.")
