# Testing Superset Backend Config Changes

## Overview
How to test changes to `superset/config.py` and other backend configuration files in the Superset project.

## Prerequisites
- Python 3.9+ with pip
- Install superset in editable mode: `pip install -e ".[dev]"`
- Install pre-commit: `pip install pre-commit`
- Install ruff: `pip install ruff`

## Running Unit Tests

Superset's `tests/conftest.py` requires the full app to be importable (including `superset_core`). For config-level unit tests that only need the config module:

```bash
# Use --noconftest to skip the heavy conftest that needs full app setup
pytest tests/unit_tests/smtp_config_test.py -v --noconftest
```

If you need the full test infrastructure, install all dependencies:
```bash
pip install -e ".[dev]"
```

## Testing Config Module Changes

The config module (`superset/config.py`) imports from several `superset.*` submodules. To test config values that depend on environment variables:

1. Use `unittest.mock.patch.dict(os.environ, ...)` to set env vars
2. Use `importlib.reload(cfg)` to re-evaluate the module-level assignments
3. Assert both value and type (e.g., `SMTP_PORT` should be `int`, not `str`)

Example pattern:
```python
import importlib, os
from unittest.mock import patch

def test_config_reads_from_env() -> None:
    with patch.dict(os.environ, {"MY_ENV_VAR": "value"}):
        import superset.config as cfg
        importlib.reload(cfg)
        assert cfg.MY_SETTING == "value"
```

## Pre-commit Validation (Required Before Pushing)

```bash
git add <changed_files>
pre-commit run --files <changed_files>
```

Common issues:
- `ruff` or `ruff-format` not found → `pip install ruff`
- mypy failures need manual fixes
- Some hooks auto-fix files; re-stage and re-run if needed

## Adversarial Testing Patterns for Config

When replacing hardcoded values with env var reads:
1. **Verify env var is read**: Set env var, reload, assert new value
2. **Verify default when unset**: Clear env, reload, assert expected default
3. **Verify old value is gone**: `grep` for the old hardcoded value to confirm removal
4. **Verify type correctness**: For numeric configs, assert `type(value) is int` not just the value
5. **Verify env example files**: Check `docker/.env` or similar files include the new variables

## Devin Secrets Needed
None required for backend config testing.
