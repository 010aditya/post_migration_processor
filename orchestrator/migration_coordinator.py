# orchestrator/migration_coordinator.py

from agents import (
    precondition_validator,
    context_collector,
    enterprise_indexer,
    reference_promoter,
    dependency_mapper,
    chunk_planner,
    fix_and_compile,
    gradle_setup,
    build_fixer,
    swagger_generator,
    test_generator,
    datasource_extractor,
    migration_reporter
)

def run_migration_pipeline():
    print("\n🚀 Starting Migration Assist Pipeline\n")

    precondition_validator()
    context_collector()
    enterprise_indexer()
    reference_promoter()
    dependency_mapper()
    chunk_planner()
    fix_and_compile()
    gradle_setup()
    build_fixer()
    swagger_generator()
    test_generator()
    datasource_extractor()
    migration_reporter()

    print("\n✅ Migration Complete. Final report written to output/final_migration_report.json\n")
