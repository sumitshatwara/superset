# Testing Python Backend Config Changes in Superset

This skill covers how to test changes to `superset/config.py` and other Python backend configuration.

## Prerequisites

1. Clone the repo and install the Python package:
   ```bash
   pip install -e .
   pip install pytest pytest-mock
   ```
2. Install and run pre-commit hooks (required before pushing):
   ```bash
   pip install ruff pre-commit
   pre-commit install
   ```

## Running Pre-commit Checks

Per AGENTS.md, **always run pre-commit before pushing**:
```bash
git add <changed-files>
pre-commit run --files <changed-files>
```

Key hooks: mypy, ruff, ruff-format, pylint. If `ruff` is not found, install it with `pip install ruff`.

## Testing Config Values

Config values in `superset/config.py` are evaluated at module import time. To test different environment states:

```python
import importlib
import os
from unittest.mock import patch

with patch.dict(os.environ, {"SUPERSET_ENV": "production"}, clear=True):
    import superset.config as cfg
    importlib.reload(cfg)
    assert cfg.SOME_CONFIG_VALUE is True

# Always restore the module after testing
importlib.reload(cfg)
```

Use `pytest.mark.parametrize` for testing multiple environment states in a single test function.

## Running Unit Tests

```bash
# Run specific test
python -m pytest tests/unit_tests/config_test.py::test_name -v

# Run all config tests
python -m pytest tests/unit_tests/config_test.py -v
```

## Test File Location

- Config tests: `tests/unit_tests/config_test.py`
- Test conftest (disables rate limiting for tests): `tests/unit_tests/conftest.py`
- Integration test config override: `tests/integration_tests/superset_test_config.py`

## Notes

- This fork might not have CI checks configured. Verify with `git(action="pr_checks")`.
- Config-only changes are shell-only testing (no browser/recording needed).
- The `tests/unit_tests/conftest.py` sets `RATELIMIT_ENABLED = False` for test isolation — be aware of this when testing rate limit config.

## Devin Secrets Needed

No secrets required for Python backend config testing.
