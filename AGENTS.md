# AGENTS.md — AI-Manager-For-Termux

## Project Overview
`AI-Manager-For-Termux` is a cross-platform toolkit designed for managing, configuring, and optimizing Android Termux and Arch Linux environments. It provides interactive terminal user interfaces (TUIs), system package orchestrators (`expac_master`, `universal_installer`), fish shell configuration repair tools (`protocol_fixer`), and aesthetic terminal enhancements.

- **Target Platforms:** Android Termux (ARM64), Arch Linux / CachyOS, Fedora Linux (development).
- **Core Script Directory:** `Scripts/`
- **Test Directory:** `tests/`

---

## Technical Stack & Dependencies
- **Languages:** Python 3.10+, Bash, Fish shell scripts.
- **Python Standard Library:** `subprocess`, `shutil`, `re`, `glob`, `os`, `sys`, `time`.
- **Testing Framework:** `pytest` (with mocking for shell execution and environment APIs).

---

## Agent Guidance & Invariant Rules
- **Canonical Agent Configuration:**
  `AGENTS.md` in the repository root is canonical. `CLAUDE.md`, `GEMINI.md`, and `.cursorrules` are symlinks pointing directly to this file.
- **Terminal Aesthetics & ANSI Standards:**
  Preserve ANSI color codes and layout functions defined in `Scripts/utils.py:Colors`. Avoid unbuffered stdout writes that break interactive TUIs.
- **Verification Rule:**
  Never commit changes without running `pytest tests/` and verifying 100% pass rates.

---

## Verification Runbooks
```bash
# Navigate to repository root
cd /home/daripper/Projects/AI-Manager-For-Termux

# Run full automated test suite
pytest tests/

# Execute interactive universal installer syntax check
python3 -m py_compile Scripts/universal_installer.py Scripts/utils.py Scripts/protocol_fixer.py
```
