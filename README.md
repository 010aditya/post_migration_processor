# 🧠 Migration Assist Tool

A modular, LLM-powered assistant to fix, complete, and compile partially migrated legacy Java applications (EJB, Struts, JSP, iBatis) into fully working Spring Boot projects.

---

## 🚀 Key Features

- ✅ Auto-fixes broken or incomplete migrated Java code
- ⭮️ Builds and retries until code compiles
- 🔗 Wires controllers, services, and repositories
- ⚙️ Generates `build.gradle`, `application.yaml`, and Swagger annotations
- 🧪 Generates scaffolded JUnit tests
- 📜 Final migration report with unresolved issues and fix logs

---

## 📁 Input Folder Structure

```plaintext
.
├── legacy/                        # Your original legacy Java codebase
├── output/                        # Partially migrated Spring Boot code
├── reference_migrations/         # (Optional) Manually migrated pairs
│   ├── project1/
│   │   ├── legacy/
│   │   └── migrated/
├── enterprise/                   # (Optional) Spring Boot base framework
├── mapping.json                  # File-to-file legacy → migrated map
├── .env                          # Environment configuration
```

---

## ⚙️ How to Run

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r migration_assist/requirements.txt
```

### 2. Set environment variables in `.env`

```dotenv
LEGACY_DIR=legacy
MIGRATED_DIR=output
MAPPING_FILE=mapping.json
REFERENCE_DIR=reference_migrations
ENTERPRISE_FRAMEWORK_DIR=enterprise

LLM_PROVIDER=openai
OPENAI_API_KEY=your-key
# or for Azure:
# AZURE_OPENAI_API_KEY=...
# AZURE_OPENAI_ENDPOINT=...
# AZURE_DEPLOYMENT_NAME=gpt-4o
```

### 3. Run the tool

```bash
python migration_assist/scripts/run_tool.py
```

Or launch via VS Code ▶️ with `.vscode/launch.json` already configured.

---

## 📆 Outputs

- Updated `output/` folder with working, buildable code
- ✅ Fixed classes with completed logic and wiring
- ✅ Swagger annotations added
- ✅ `build.gradle` generated or corrected
- ✅ `application.yaml` with datasource configs
- ✅ `src/test/java` with basic JUnit tests
- 📄 `migration_assist/output/final_migration_report.json` with fix logs and unresolved flags

---

## 🧠 Technology Stack

- Python 3.9+
- OpenAI / Azure OpenAI (GPT-4o)
- Spring Boot 3.2+
- Gradle
- javalang + tenacity + dotenv

---

## 🤝 Contributing

1. Fork this repo
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Push to the branch
5. Open a pull request 🚀
