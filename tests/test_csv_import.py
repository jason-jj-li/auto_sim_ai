"""Auto-parsing CSV import — any columns, no required schema.

personas_from_dataframe maps known columns (incl. Chinese aliases) to persona
fields, splits list fields, and keeps every unknown column as a custom attribute
that flows into the persona card and the LLM prompt. Before this, uploads were
rejected unless they had ID/age/gender, and unknown columns were only dumped
into background prose.
"""
import pandas as pd

from src.persona import personas_from_dataframe


def test_any_csv_parses_without_required_columns():
    df = pd.DataFrame({"city": ["Boston", "SF"], "income_bracket": ["high", "low"]})
    ps = personas_from_dataframe(df)
    assert [p.name for p in ps] == ["Person_001", "Person_002"]
    assert all(p.age == 30 and p.gender == "Unknown" for p in ps)
    assert ps[0].city == "Boston" and ps[0].income_bracket == "high"
    assert "city" in ps[0].to_dict()                      # extras roundtrip
    assert '"city": "Boston"' in ps[0].to_prompt_context()  # extras reach the prompt


def test_known_columns_aliases_and_age_ranges():
    df = pd.DataFrame({
        "姓名": ["张三"], "age": ["25-34"], "gender": ["F"],
        "occupation": ["teacher"], "personality_traits": ["calm; analytical"],
        "values": ["family, honesty"],
    })
    p = personas_from_dataframe(df)[0]
    assert p.name == "张三" and p.age == 29 and p.gender == "F" and p.occupation == "teacher"
    assert p.personality_traits == ["calm", "analytical"]
    assert p.values == ["family", "honesty"]
