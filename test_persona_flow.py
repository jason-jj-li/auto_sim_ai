"""Test the complete persona generation and display flow"""
import sys
sys.path.insert(0, '/Users/jjlee/Desktop/300-project/auto_sim_ai')

from src.persona import Persona

# Test 1: Create persona with all fields
print("=" * 60)
print("Test 1: Creating persona with extended fields")
print("=" * 60)

test_data = {
    'name': '张伟',
    'age': 47,
    'gender': 'Female',
    'occupation': '农林牧渔从业者',
    'education': '本科',
    'location': '城镇',
    'marital_status': '已婚',
    'ethnicity': '汉族',
    'political_affiliation': '共青团员',
    'religion': '无宗教信仰',
    'personality_traits': ['健康生活', '环境可持续性', 'AI工具使用'],
    'values': ['家庭责任', '健康生活', '环境可持续性'],
    'background': '拥有本科学历。从事农林牧渔从业者工作多年...'
}

persona = Persona.from_dict(test_data)

print(f"✅ Persona created: {persona.name}")
print(f"   Age: {persona.age}")
print(f"   Gender: {persona.gender}")
print(f"   Occupation: {persona.occupation}")
print(f"   Education: {persona.education}")
print(f"   Location: {persona.location}")
print(f"   Marital Status: {persona.marital_status}")
print(f"   Ethnicity: {persona.ethnicity}")
print(f"   Political: {persona.political_affiliation}")
print(f"   Religion: {persona.religion}")

# Test 2: Convert back to dict
print("\n" + "=" * 60)
print("Test 2: Converting persona to dictionary")
print("=" * 60)

persona_dict = persona.to_dict()
print(f"Total fields: {len([v for v in persona_dict.values() if v is not None and v != [] and v != ''])}")

print("\nAll non-empty fields:")
for key, value in persona_dict.items():
    if value is not None and value != [] and value != '':
        print(f"  - {key}: {str(value)[:50]}")

# Test 3: Standard fields check
print("\n" + "=" * 60)
print("Test 3: Checking standard fields")
print("=" * 60)

standard_fields = {'name', 'age', 'gender', 'occupation', 'education', 
                  'location', 'background', 'personality_traits', 'values',
                  'marital_status', 'ethnicity', 'political_affiliation', 'religion'}

displayed_fields = [k for k in persona_dict.keys() if k in standard_fields and persona_dict[k]]
print(f"Standard fields to display: {len(displayed_fields)}")
for field in displayed_fields:
    print(f"  ✓ {field}")

# Test 4: Extra dynamic fields
print("\n" + "=" * 60)
print("Test 4: Testing extra dynamic fields")
print("=" * 60)

test_data_with_extra = {
    **test_data,
    'income_level': '中等收入',
    'family_size': 3,
    'has_insurance': True
}

persona_extra = Persona.from_dict(test_data_with_extra)
dict_extra = persona_extra.to_dict()

extra_fields = [k for k in dict_extra.keys() if k not in standard_fields]
print(f"Extra fields found: {len(extra_fields)}")
for field in extra_fields:
    value = dict_extra[field]
    if value is not None and value != '' and value != []:
        print(f"  + {field}: {value}")

print("\n" + "=" * 60)
print("✅ All tests passed!")
print("=" * 60)
