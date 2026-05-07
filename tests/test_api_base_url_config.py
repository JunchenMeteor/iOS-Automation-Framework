import os

import pytest

from conftest import api_base_url


def test_api_base_url_uses_environment_override(monkeypatch):
    monkeypatch.setenv("API_BASE_URL", "https://override.example.test")

    value = api_base_url.__wrapped__({"api": {"base_url": "https://yaml.example.test"}})

    assert value == "https://override.example.test"


def test_api_base_url_falls_back_to_environment_yaml(monkeypatch):
    monkeypatch.delenv("API_BASE_URL", raising=False)

    value = api_base_url.__wrapped__({"api": {"base_url": "https://yaml.example.test"}})

    assert value == "https://yaml.example.test"

