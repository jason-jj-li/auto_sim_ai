"""Retry + error-reason contract for the LLM clients.

AsyncLLMClient.generate_response_async returns (text, None) or (None, reason)
and retries transient failures (429/5xx/timeout) with backoff — parallel bursts
against cloud APIs hit rate limits, and before this every blip became a silent
"[Error: No response]" row. LMStudioClient keeps returning None on failure but
records the reason in .last_error for the sequential engine.
"""
import asyncio

import aiohttp

from src.llm_client import AsyncLLMClient, LMStudioClient


class _FakeResp:
    def __init__(self, status, data=None, text="boom"):
        self.status = status
        self._data = data or {}
        self._text = text

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    async def json(self):
        return self._data

    async def text(self):
        return self._text


class _FakeSession:
    """Plays back a scripted list of (status, data) or "timeout" per POST."""
    calls = 0
    script = []

    def __init__(self, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    def post(self, *a, **k):
        _FakeSession.calls += 1
        item = _FakeSession.script.pop(0)
        if item == "timeout":
            raise asyncio.TimeoutError()
        status, data = item
        return _FakeResp(status, data)


def _script(monkeypatch, script):
    _FakeSession.calls = 0
    _FakeSession.script = list(script)
    monkeypatch.setattr(aiohttp, "ClientSession", _FakeSession)

    async def _no_sleep(*a):
        pass

    monkeypatch.setattr(asyncio, "sleep", _no_sleep)


def _run(coro):
    return asyncio.run(coro)


def test_async_retries_429_then_succeeds(monkeypatch):
    _script(monkeypatch, [(429, None), (429, None), (200, {"choices": [{"message": {"content": "ok"}}]})])
    text, err = _run(AsyncLLMClient("https://api.deepseek.com/v1", "k").generate_response_async("q"))
    assert text == "ok" and err is None
    assert _FakeSession.calls == 3


def test_async_400_fails_fast_with_reason(monkeypatch):
    _script(monkeypatch, [(400, None)])
    text, err = _run(AsyncLLMClient("https://api.deepseek.com/v1", "k").generate_response_async("q"))
    assert text is None and "HTTP 400" in err
    assert _FakeSession.calls == 1  # no payload variants, no retries


def test_async_timeout_exhausts_retries(monkeypatch):
    _script(monkeypatch, ["timeout", "timeout", "timeout"])
    text, err = _run(AsyncLLMClient("https://api.deepseek.com/v1", "k").generate_response_async("q"))
    assert text is None and "TimeoutError" in err
    assert _FakeSession.calls == 3


def test_async_empty_completion_retried_then_succeeds(monkeypatch):
    empty = (200, {"choices": [{"message": {"content": ""}, "finish_reason": "stop"}]})
    _script(monkeypatch, [empty, (200, {"choices": [{"message": {"content": "ok"}}]})])
    text, err = _run(AsyncLLMClient("https://api.deepseek.com/v1", "k").generate_response_async("q"))
    assert text == "ok" and err is None
    assert _FakeSession.calls == 2


def test_async_empty_completion_exhausts_with_reason(monkeypatch):
    empty = (200, {"choices": [{"message": {"content": ""}, "finish_reason": "stop"}]})
    _script(monkeypatch, [empty, empty, empty])
    text, err = _run(AsyncLLMClient("https://api.deepseek.com/v1", "k").generate_response_async("q"))
    assert text is None and "empty completion" in err
    assert _FakeSession.calls == 3


def test_async_length_truncation_fails_fast_with_guidance(monkeypatch):
    """finish_reason=length with empty content = reasoning model burned the whole
    token budget — deterministic, must NOT retry, and the reason must say so."""
    truncated = (200, {"choices": [{"message": {"content": ""}, "finish_reason": "length"}]})
    _script(monkeypatch, [truncated, truncated, truncated])
    text, err = _run(AsyncLLMClient("https://api.deepseek.com/v1", "k").generate_response_async("q"))
    assert text is None and "finish_reason=length" in err and "Max Tokens" in err
    assert _FakeSession.calls == 1  # no retries on a deterministic failure


def test_sync_last_error_records_reason(monkeypatch):
    client = LMStudioClient("https://api.deepseek.com/v1", "sk-x")

    class _Boom:  # attribute chain client.chat.completions.create(...) raises
        class chat:
            class completions:
                @staticmethod
                def create(**k):
                    raise RuntimeError("sdk down")

    client.client = _Boom()

    class _Resp:
        status_code = 429
        text = "rate limited"

    monkeypatch.setattr("requests.post", lambda *a, **k: _Resp())
    assert client.chat_completion([{"role": "user", "content": "hi"}]) is None
    assert "HTTP 429" in client.last_error
