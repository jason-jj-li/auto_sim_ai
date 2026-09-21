"""Structured-distributions extraction path.

The extraction LLM now returns {"distributions": {field: {categories, probabilities}}}
which must drive persona generation directly (hand-regex parsers are fallback only),
and sampled custom variables must surface in the persona's prompt context as
structured fields — before this, unknown fields fell through the regex chain and
leaked as raw "Mixed (<30k 30%, ...)" strings into the background prose.
"""
from collections import Counter

from src.persona import Persona
from src.persona_generator import PersonaGenerator


def _extracted():
    return {
        "sample_size": "50",
        "age_range": "18-40",
        "distributions": {
            "life_satisfaction": {"categories": ["satisfied", "neutral", "dissatisfied"],
                                  "probabilities": [0.45, 0.35, 0.20]},
            "gender": {"categories": ["male", "female"], "probabilities": [48, 52]},  # percent -> normalized
            "uniform_field": {"categories": ["a", "b"]},                              # no probs -> uniform
            "broken_field": {"categories": "notalist"},                               # malformed -> skipped
        },
    }


def test_structured_distributions_drive_generation():
    personas = PersonaGenerator.generate_personas_from_ai_extraction(_extracted(), n=60, seed=1)
    assert len(personas) == 60

    sat = [p["life_satisfaction"] for p in personas]
    assert set(sat) == {"satisfied", "neutral", "dissatisfied"}
    assert Counter(sat).most_common(1)[0][0] == "satisfied"  # 45% is the modal category

    assert {p["gender"] for p in personas} == {"male", "female"}
    assert {p["uniform_field"] for p in personas} == {"a", "b"}
    assert all("broken_field" not in p for p in personas)

    # no raw distribution spec leaks into prose
    assert all("%" not in p["background"] for p in personas)


def test_structured_distributions_beat_hand_parsers():
    """A legacy top-level string the hand-regex would mangle loses to the structured entry."""
    data = _extracted()
    data["gender"] = "Mixed"  # hand parser would produce garbage; distributions.gender must win
    personas = PersonaGenerator.generate_personas_from_ai_extraction(data, n=20, seed=2)
    assert {p["gender"] for p in personas} == {"male", "female"}


def test_prompt_context_includes_extra_attributes():
    p = Persona.from_dict({
        "name": "T", "age": 30, "gender": "F", "occupation": "X", "background": "b",
        "personality_traits": [], "values": [], "life_satisfaction": "satisfied",
    })
    ctx = p.to_prompt_context()
    assert '"life_satisfaction": "satisfied"' in ctx


def test_age_group_drives_integer_age():
    """The bracket is the single source of age — no more 'age 69 vs age_group 30-44'."""
    data = {"distributions": {
        "age_group": {"categories": ["18-29", "30-44", "60+"], "probabilities": [0.5, 0.3, 0.2]},
    }}
    ps = PersonaGenerator.generate_personas_from_ai_extraction(data, n=40, seed=3)
    bounds = {"18-29": (18, 29), "30-44": (30, 44), "60+": (60, 89)}
    assert len(ps) == 40
    for p in ps:
        lo, hi = bounds[p["age_group"]]
        assert lo <= p["age"] <= hi


def test_conditional_field_follows_parent():
    data = {"distributions": {
        "age_group": {"categories": ["18-29", "60+"], "probabilities": [0.5, 0.5]},
        "employment": {"conditioned_on": "age_group", "table": {
            "18-29": {"categories": ["student", "employed"], "probabilities": [0.7, 0.3]},
            "60+": {"categories": ["retired"], "probabilities": [1.0]},
        }},
    }}
    ps = PersonaGenerator.generate_personas_from_ai_extraction(data, n=30, seed=4)
    assert len(ps) == 30
    for p in ps:
        if p["age_group"] == "60+":
            assert p["employment"] == "retired"
            assert p["age"] >= 60
        else:
            assert p["employment"] in {"student", "employed"}


def test_none_labels_stay_out_of_background():
    data = {"distributions": {
        "religion": {"categories": ["none"], "probabilities": [1.0]},
        "ethnicity": {"categories": ["han"], "probabilities": [1.0]},
        "marital_status": {"categories": ["single"], "probabilities": [1.0]},
        "education": {"categories": ["senior high"], "probabilities": [1.0]},
    }}
    p = PersonaGenerator.generate_personas_from_ai_extraction(data, n=1, seed=5)[0]
    bg = p["background"]
    assert "信仰" not in bg and "民族" not in bg      # none/han suppressed
    assert "单身" in bg and "高中" in bg               # English labels mapped to Chinese prose
