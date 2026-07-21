# Using UV with Homework 3

## 🎯 Why UV?

**uv** is a fast Python package manager that:
- ✅ **10-100x faster** than pip
- ✅ **Automatic virtual environment** management
- ✅ **Lock file support** for reproducible builds
- ✅ **Drop-in replacement** for pip
- ✅ **Modern tooling** used in AI Engineering courses

## 🚀 Quick Start with UV

### 1. Install Dependencies
```bash
uv sync
```

This will:
- Create a virtual environment (`.venv`)
- Install all dependencies from `pyproject.toml`
- Generate a `uv.lock` file for reproducibility

### 2. Run Scripts
```bash
uv run main.py
uv run verify_setup.py
uv run finetune_openai.py
```

The `uv run` command:
- Automatically uses the project's virtual environment
- No need to activate `.venv` manually
- Works seamlessly across platforms

### 3. Add Dependencies (if needed)
```bash
uv add package-name
```

## 📋 UV Commands Cheat Sheet

| Task | UV Command | Pip Equivalent |
|------|-----------|----------------|
| Install deps | `uv sync` | `pip install -r requirements.txt` |
| Run script | `uv run script.py` | `python script.py` |
| Add package | `uv add package` | `pip install package` |
| Remove package | `uv remove package` | `pip uninstall package` |
| Show installed | `uv pip list` | `pip list` |
| Create venv | `uv venv` | `python -m venv .venv` |

## 🔄 Migration from Pip

The project now supports **both** uv and pip:

### Using UV (Recommended)
```bash
uv sync                  # Install
uv run main.py           # Run
```

### Using Pip (Alternative)
```bash
pip install -r requirements.txt  # Install
python main.py                   # Run
```

## 📁 Project Structure with UV

```
Homework 3/
├── pyproject.toml       # 🆕 Project metadata & dependencies
├── .python-version      # 🆕 Python version (3.12)
├── uv.lock              # 🆕 Auto-generated lock file
├── requirements.txt     # ✅ Kept for pip compatibility
├── .venv/               # 🆕 Auto-created by uv
└── ...
```

## 💡 Benefits Over Pip

1. **Speed**: 10-100x faster installation
2. **Reliability**: Lock file ensures everyone uses same versions
3. **Simplicity**: No manual venv activation needed
4. **Modern**: Industry standard for Python projects
5. **Compatible**: Works alongside pip if needed

## 🔧 Installation

### Install UV

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Using pip:**
```bash
pip install uv
```

**Using pipx:**
```bash
pipx install uv
```

## 🎓 Example Workflow

```bash
# 1. Clone/navigate to project
cd "C:\Users\Admin\Documents\Training\AI Engineering\AI-Engineering-Training\Homework 3"

# 2. Install dependencies with uv
uv sync

# 3. Create .env file with your API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-actual-key-here

# 4. Test .env loading (optional)
uv run test_env.py

# 5. Verify setup
uv run verify_setup.py

# 6. Run the pipeline
uv run main.py

# 7. Run individual scripts
uv run finetune_openai.py
uv run benchmark_models.py
uv run generate_excel_report.py
```

## ❓ FAQ

### Q: Do I need to activate the virtual environment?
**A:** No! `uv run` automatically uses the project's `.venv`

### Q: Can I still use pip?
**A:** Yes! The project maintains `requirements.txt` for pip compatibility

### Q: Where is the virtual environment?
**A:** In `.venv/` directory (created automatically by `uv sync`)

### Q: What if uv is not available?
**A:** Use pip commands as shown in the documentation

### Q: How do I update dependencies?
**A:** `uv sync --upgrade` or `uv add package@latest`

## 📚 Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [UV GitHub](https://github.com/astral-sh/uv)
- [UV Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)

---

**Bottom Line:** UV makes Python dependency management fast, reliable, and simple! 🚀
