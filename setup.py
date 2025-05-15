# setup.py

from setuptools import setup, find_packages

setup(
    name="migration_assist",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "openai>=1.0.0",
        "tenacity>=8.2.0",
        "javalang>=0.13.0",
        "pyyaml>=6.0.0",
        "tqdm>=4.66.0"
    ],
    entry_points={
        "console_scripts": [
            "migration-assist=migration_assist.scripts.run_tool:main"
        ]
    }
)
