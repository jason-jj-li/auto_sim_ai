"""Regression tests for identity, validation, assignment, and persistence."""
from datetime import datetime

import pandas as pd

from src.ab_testing import ABTestManager, Condition
from src.longitudinal_study import ConversationHistory
from src.persona import Persona
from src.reliability import question_collapse_report
from src.simulation import SimulationEngine, SimulationResult
from src.storage import ResultsStorage, results_to_wide


def _persona(name, persona_id):
    return Persona(
        name=name, age=30, gender="X", occupation="Tester", background="b",
        personality_traits=[], values=[], persona_id=persona_id,
    )


def test_duplicate_names_remain_distinct_in_ab_assignment():
    people = [_persona("Same Name", f"p-{i}") for i in range(6)]
    conditions = [Condition("a", "A", "a"), Condition("b", "B", "b")]
    assignments = ABTestManager(seed=7).assign_personas(people, conditions)
    assert set(assignments) == {p.persona_id for p in people}
    assert sorted(assignments.values()).count("a") == 3
    assert sorted(assignments.values()).count("b") == 3


def test_invalid_numeric_response_is_not_fabricated():
    cleaned, valid, error = SimulationEngine._validate_response(
        "My answer is 12", {"type": "number", "min": 1, "max": 5}
    )
    assert cleaned == "My answer is 12"
    assert valid is False
    assert "outside" in error


def test_collapse_report_excludes_invalid_and_errors():
    df = pd.DataFrame({
        "question": ["q"] * 4,
        "response": ["yes", "yes", "bad", "[Error: timeout]"],
        "validation_status": ["valid", "valid", "invalid", "not_requested"],
    })
    report = question_collapse_report(df).iloc[0]
    assert report["n"] == 2
    assert report["invalid_or_failed"] == 2


def test_zero_response_run_still_has_discoverable_csv(tmp_path):
    storage = ResultsStorage(str(tmp_path))
    result = SimulationResult("survey", datetime.now().isoformat())
    csv_name, _ = storage.save_results(result, "empty")
    assert (tmp_path / csv_name).exists()
    assert storage.list_results()[0]["n_responses"] == 0


def test_longitudinal_history_trim_keeps_system_and_recent_messages():
    history = ConversationHistory("P", "p")
    history.add_system_message("persona")
    for i in range(10):
        history.add_user_message(str(i))
    messages = history.get_messages(max_messages=5)
    assert len(messages) == 5
    assert messages[0] == {"role": "system", "content": "persona"}
    assert [m["content"] for m in messages[1:]] == ["6", "7", "8", "9"]


def test_wide_results_keep_complete_population_and_answers():
    frame = pd.DataFrame([
        {'persona_id': 'p1', 'persona_name': 'A', 'persona_age': 30,
         'persona_income': 'high', 'persona_values': '["care"]',
         'question': 'Q1', 'response': 'Yes', 'condition': 'Treatment'},
        {'persona_id': 'p1', 'persona_name': 'A', 'persona_age': 30,
         'persona_income': 'high', 'persona_values': '["care"]',
         'question': 'Q2', 'response': '4', 'condition': 'Treatment'},
    ])
    wide = results_to_wide(frame)
    assert len(wide) == 1
    assert wide.loc[0, 'persona_income'] == 'high'
    assert wide.loc[0, 'persona_values'] == '["care"]'
    assert wide.loc[0, 'study_condition'] == 'Treatment'
    assert wide.loc[0, 'answer__Q1'] == 'Yes'
    assert wide.loc[0, 'answer__Q2'] == '4'
