"""Test AI demographic extraction functionality."""
import json
from src.persona_generator import PersonaGenerator

# Test the AI extraction prompt generation
test_text = """
We're studying college students aged 18-24 in California universities. 
The population is approximately 60% female and 40% male, mostly majoring 
in STEM fields (Computer Science, Engineering, Biology). Most are from 
middle to upper-middle-class families with household incomes between 
$75,000-$150,000. They value education, career success, and work-life 
balance. Common interests include technology, social media, fitness, 
and environmental sustainability.
"""

print("=" * 80)
print("Testing AI Demographic Extraction")
print("=" * 80)
print("\nInput Text:")
print("-" * 80)
print(test_text)
print("-" * 80)

# Test without actual LLM (just show the structure would work)
print("\nThis feature will:")
print("1. ✅ Send text to LLM for demographic extraction")
print("2. ✅ Parse JSON response with demographic attributes")
print("3. ✅ Generate personas based on extracted demographics")
print("4. ✅ Display generated personas in the UI")

print("\nExpected extraction result structure:")
expected_structure = {
    "age_range": "18-24",
    "gender": "Mixed (60% female, 40% male)",
    "occupation": "College Students",
    "education": "Pursuing Bachelor's",
    "location": "California universities",
    "income_range": "$75,000-$150,000",
    "sample_size": "Not specified",
    "interests": ["Technology", "Social media", "Fitness", "Environmental sustainability"],
    "values": ["Education", "Career success", "Work-life balance"]
}

print(json.dumps(expected_structure, indent=2))

print("\n" + "=" * 80)
print("To test with real LLM:")
print("=" * 80)
print("1. Start the Streamlit app: streamlit run app.py")
print("2. Connect to LLM on Home page")
print("3. Go to Setup page → Generate Personas tab")
print("4. Select 'AI-Powered Extraction' sub-tab")
print("5. Paste your text and click 'Extract Demographics & Generate Personas'")
print("=" * 80)
