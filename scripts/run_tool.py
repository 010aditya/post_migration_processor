# scripts/run_tool.py

import sys
import os

# Ensure core and agents are importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator.migration_coordinator import run_migration_pipeline

if __name__ == "__main__":
    run_migration_pipeline()
