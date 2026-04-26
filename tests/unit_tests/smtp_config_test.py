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
import importlib
import os
from unittest.mock import patch


def test_smtp_password_reads_from_env() -> None:
    """SMTP_PASSWORD should be sourced from the SUPERSET_SMTP_PASSWORD env var."""
    with patch.dict(os.environ, {"SUPERSET_SMTP_PASSWORD": "s3cure!"}):
        import superset.config as cfg

        importlib.reload(cfg)
        assert cfg.SMTP_PASSWORD == "s3cure!"  # noqa: S105


def test_smtp_password_defaults_to_empty_string() -> None:
    """SMTP_PASSWORD should default to an empty string when env var is unset."""
    env = os.environ.copy()
    env.pop("SUPERSET_SMTP_PASSWORD", None)
    with patch.dict(os.environ, env, clear=True):
        import superset.config as cfg

        importlib.reload(cfg)
        assert cfg.SMTP_PASSWORD == ""


def test_smtp_host_reads_from_env() -> None:
    """SMTP_HOST should be sourced from the SUPERSET_SMTP_HOST env var."""
    with patch.dict(os.environ, {"SUPERSET_SMTP_HOST": "mail.example.com"}):
        import superset.config as cfg

        importlib.reload(cfg)
        assert cfg.SMTP_HOST == "mail.example.com"


def test_smtp_user_reads_from_env() -> None:
    """SMTP_USER should be sourced from the SUPERSET_SMTP_USER env var."""
    with patch.dict(os.environ, {"SUPERSET_SMTP_USER": "admin@example.com"}):
        import superset.config as cfg

        importlib.reload(cfg)
        assert cfg.SMTP_USER == "admin@example.com"


def test_smtp_port_reads_from_env() -> None:
    """SMTP_PORT should be sourced from the SUPERSET_SMTP_PORT env var as int."""
    with patch.dict(os.environ, {"SUPERSET_SMTP_PORT": "587"}):
        import superset.config as cfg

        importlib.reload(cfg)
        assert cfg.SMTP_PORT == 587


def test_smtp_mail_from_reads_from_env() -> None:
    """SMTP_MAIL_FROM should be sourced from the SUPERSET_SMTP_MAIL_FROM env var."""
    with patch.dict(os.environ, {"SUPERSET_SMTP_MAIL_FROM": "no-reply@example.com"}):
        import superset.config as cfg

        importlib.reload(cfg)
        assert cfg.SMTP_MAIL_FROM == "no-reply@example.com"
