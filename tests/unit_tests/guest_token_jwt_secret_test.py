# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

import importlib
import inspect
import os
from unittest.mock import MagicMock, patch

import pytest

from superset.initialization import SupersetAppInitializer

SAMPLE_SECRET = "my-secret-123"  # noqa: S105


def test_guest_token_jwt_secret_reads_from_env() -> None:
    """GUEST_TOKEN_JWT_SECRET should be populated from the env var."""
    with patch.dict(os.environ, {"SUPERSET_GUEST_TOKEN_JWT_SECRET": SAMPLE_SECRET}):
        import superset.config as cfg

        importlib.reload(cfg)
        assert cfg.GUEST_TOKEN_JWT_SECRET == SAMPLE_SECRET


def test_guest_token_jwt_secret_defaults_to_empty() -> None:
    """GUEST_TOKEN_JWT_SECRET should default to an empty string when unset."""
    env = os.environ.copy()
    env.pop("SUPERSET_GUEST_TOKEN_JWT_SECRET", None)
    with patch.dict(os.environ, env, clear=True):
        import superset.config as cfg

        importlib.reload(cfg)
        assert cfg.GUEST_TOKEN_JWT_SECRET == ""


def test_guest_token_jwt_secret_no_hardcoded_value() -> None:
    """The old hardcoded default must not appear anywhere in config.py."""
    import superset.config as cfg

    source = inspect.getsource(cfg)
    assert "test-guest-secret-change-me" not in source


def _make_app_init(
    *, debug: bool, testing: bool, secret: str
) -> SupersetAppInitializer:
    app_init = object.__new__(SupersetAppInitializer)
    mock_app = MagicMock()
    mock_app.debug = debug
    mock_app.config = {
        "TESTING": testing,
        "GUEST_TOKEN_JWT_SECRET": secret,
    }
    app_init.superset_app = mock_app
    app_init.config = mock_app.config
    return app_init


def test_check_guest_token_jwt_secret_raises_in_production() -> None:
    """RuntimeError raised when secret is empty in non-debug, non-test mode."""
    app_init = _make_app_init(debug=False, testing=False, secret="")

    with patch("superset.initialization.is_test", return_value=False):
        with pytest.raises(RuntimeError, match="SUPERSET_GUEST_TOKEN_JWT_SECRET"):
            app_init.check_guest_token_jwt_secret()


def test_check_guest_token_jwt_secret_allows_debug_mode() -> None:
    """Empty secret should only warn (not raise) in debug mode."""
    app_init = _make_app_init(debug=True, testing=False, secret="")

    with patch("superset.initialization.is_test", return_value=False):
        app_init.check_guest_token_jwt_secret()


def test_check_guest_token_jwt_secret_passes_with_secret() -> None:
    """No error when a valid secret is provided."""
    app_init = _make_app_init(debug=False, testing=False, secret=SAMPLE_SECRET)

    with patch("superset.initialization.is_test", return_value=False):
        app_init.check_guest_token_jwt_secret()
