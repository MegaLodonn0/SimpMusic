# SimpMusic - Translation & Automation Wrapper

This repository is a specialized wrapper for the [SimpMusic](https://github.com/maxrave-dev/SimpMusic) project, focusing on advanced automated translations and cross-platform synchronization.

## 🚀 Key Differences from Upstream (maxrave-dev)

### 1. Automated AI Translation Suite
Unlike the original repository, this fork includes a powerful set of Python scripts designed to automate the translation process using **Claude 3.5 Haiku/Sonnet**:
- `translate_all_languages.py`: Batch translates all missing strings across 24+ languages.
- `update_all_translations.py`: Synchronizes and corrects existing translation files.
- `complete_final_11_languages.py`: Targeted scripts for finalizing specific language sets.

### 2. Enhanced i18n Support
- **Full Turkish Localization:** The Turkish (`values-tr`) translation has been completely overhauled for better accuracy and natural flow.
- **24-Language Sync:** Most languages are synchronized with the latest upstream strings, ensuring no missing UI elements in any supported region.

### 3. Development Workflow
- Includes specialized AI-driven development configurations (`.aider`, `.claude/skills`) for faster iteration and high-quality code standards.

## 🛠️ How to Use the Scripts
1. Ensure you have your AI API keys configured.
2. Run `python translate_all_languages.py` to check for missing strings.
3. The scripts will automatically update the `SimpMusic/composeApp/src/commonMain/composeResources/` directories.

---
*Maintained by [MegaLodonn0](https://github.com/MegaLodonn0)*
