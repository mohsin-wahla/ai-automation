from pydantic import BaseModel
from typing import Any


class TestCase(BaseModel):
    test_case_id: str
    title: str
    type: str
    priority: str
    preconditions: list[str]
    steps: list[str]
    test_data: dict[str, Any]
    expected_result: list[str]
    automation_candidate: bool


class TestCaseCollection(BaseModel):
    test_cases: list[TestCase]


class FailureAnalysis(BaseModel):
    classification: str
    confidence: str
    root_cause: str
    evidence: list[str]
    recommended_action: str
    healing_allowed: bool
    healing_type: str
    replacement_locator: str | None = None