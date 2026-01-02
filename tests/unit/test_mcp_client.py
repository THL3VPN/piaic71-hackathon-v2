from __future__ import annotations

# [Task]: T005 [From]: specs/019-agent-tool-chaining/spec.md User Story 1

from src.services import mcp_client


class _FakeResult:
    def __init__(self, structured_content, content):
        self.structuredContent = structured_content
        self.content = content


def test_extract_tool_result_unwraps_single_result_key() -> None:
    payload = [{"id": 1, "title": "hello world", "completed": False}]
    result = _FakeResult({"result": payload}, [])
    assert mcp_client._extract_tool_result(result) == payload


def test_extract_tool_result_preserves_non_result_payloads() -> None:
    payload = {"task_id": 1, "status": "created", "title": "milk"}
    result = _FakeResult(payload, [])
    assert mcp_client._extract_tool_result(result) == payload
