import logging
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from math_ai_agent import config


@pytest.fixture()
def tmp_config(tmp_path):
    """Write a minimal config.yaml and patch _CONFIG_PATH to point at it."""
    cfg = {
        "server": {
            "calculator_mcp": {
                "url": "http://localhost:9000/mcp",
                "is_oauth": False,
                "token_dir": "/tmp/tokens",
                "callback_port": 12345,
                "timeout": 30,
            }
        },
        "logging": {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                }
            },
            "root": {"level": "WARNING", "handlers": ["console"]},
        },
    }
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(yaml.dump(cfg))
    with patch.object(config, "_CONFIG_PATH", cfg_path):
        yield cfg


# ---------------------------------------------------------------------------
# _resolve_config_path
# ---------------------------------------------------------------------------


def test_resolve_config_path_uses_env_var(tmp_path, monkeypatch):
    custom = tmp_path / "custom.yaml"
    custom.touch()
    monkeypatch.setenv("CALCULATOR_MCP_CONFIG", str(custom))
    assert config._resolve_config_path() == custom


def test_resolve_config_path_default(monkeypatch):
    monkeypatch.delenv("CALCULATOR_MCP_CONFIG", raising=False)
    result = config._resolve_config_path()
    assert result.name == "config.yaml"


# ---------------------------------------------------------------------------
# _load_config
# ---------------------------------------------------------------------------


def test_load_config_returns_dict(tmp_config):
    result = config._load_config()
    assert isinstance(result, dict)
    assert "server" in result
    assert "logging" in result


# ---------------------------------------------------------------------------
# configure_logging
# ---------------------------------------------------------------------------


def test_configure_logging_applies_config(tmp_config):
    config.configure_logging()
    root = logging.getLogger()
    assert root.level == logging.WARNING


# ---------------------------------------------------------------------------
# get_timeout
# ---------------------------------------------------------------------------


def test_get_timeout(tmp_config):
    assert config.get_timeout() == 30


# ---------------------------------------------------------------------------
# is_oauth
# ---------------------------------------------------------------------------


def test_is_oauth_false(tmp_config):
    assert config.is_oauth() is False


def test_is_oauth_true(tmp_path):
    cfg = {
        "server": {
            "calculator_mcp": {
                "url": "http://localhost/mcp",
                "is_oauth": True,
                "token_dir": "/tmp/tokens",
                "callback_port": 10000,
                "timeout": 10,
            }
        },
        "logging": {
            "version": 1,
            "disable_existing_loggers": False,
            "root": {"level": "WARNING"},
        },
    }
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(yaml.dump(cfg))
    with patch.object(config, "_CONFIG_PATH", cfg_path):
        assert config.is_oauth() is True


def test_is_oauth_missing_defaults_false(tmp_path):
    cfg = {
        "server": {
            "calculator_mcp": {
                "url": "http://localhost/mcp",
                "token_dir": "/tmp/tokens",
                "callback_port": 10000,
                "timeout": 10,
            }
        },
        "logging": {
            "version": 1,
            "disable_existing_loggers": False,
            "root": {"level": "WARNING"},
        },
    }
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(yaml.dump(cfg))
    with patch.object(config, "_CONFIG_PATH", cfg_path):
        assert config.is_oauth() is False


# ---------------------------------------------------------------------------
# get_url
# ---------------------------------------------------------------------------


def test_get_url(tmp_config):
    assert config.get_url() == "http://localhost:9000/mcp"


# ---------------------------------------------------------------------------
# get_token_dir
# ---------------------------------------------------------------------------


def test_get_token_dir(tmp_config):
    assert config.get_token_dir() == "/tmp/tokens"


# ---------------------------------------------------------------------------
# get_callback_port
# ---------------------------------------------------------------------------


def test_get_callback_port(tmp_config):
    assert config.get_callback_port() == 12345
