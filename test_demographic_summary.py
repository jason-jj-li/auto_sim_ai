"""
Test Demographic Summary Table Feature
========================================

This script demonstrates the demographic summary functionality
that will be displayed after persona generation.
"""

from collections import Counter

# Simulated generated personas
class MockPersona:
    def __init__(self, name, age, gender, occupation, education, location):
        self.name = name
        self.age = age
        self.gender = gender
        self.occupation = occupation
        self.education = education
        self.location = location

# Create sample personas
generated_personas = [
    MockPersona("Sarah Chen", 21, "Female", "Computer Science Student", "Bachelor's", "California"),
    MockPersona("Michael Rodriguez", 19, "Male", "Engineering Student", "Bachelor's", "California"),
    MockPersona("Emma Johnson", 22, "Female", "Biology Student", "Bachelor's", "California"),
    MockPersona("James Lee", 20, "Male", "Computer Science Student", "Bachelor's", "California"),
    MockPersona("Olivia Martinez", 23, "Female", "Engineering Student", "Bachelor's", "California"),
    MockPersona("William Brown", 18, "Male", "Computer Science Student", "Bachelor's", "California"),
    MockPersona("Sophia Davis", 24, "Female", "Biology Student", "Bachelor's", "California"),
    MockPersona("Liam Wilson", 21, "Male", "Engineering Student", "Bachelor's", "California"),
    MockPersona("Ava Taylor", 22, "Female", "Computer Science Student", "Bachelor's", "California"),
    MockPersona("Noah Anderson", 20, "Male", "Biology Student", "Bachelor's", "California"),
]

print("=" * 80)
print("DEMOGRAPHIC SUMMARY TABLE - Sample Output")
print("=" * 80)
print()

# Age statistics
ages = [p.age for p in generated_personas]
age_mean = sum(ages) / len(ages)
age_min = min(ages)
age_max = max(ages)

print("📈 AGE STATISTICS")
print("-" * 40)
print(f"Mean Age: {age_mean:.1f}")
print(f"Age Range: {age_min} - {age_max}")
print()

# Gender distribution
gender_counts = Counter([p.gender for p in generated_personas])
print("⚧ GENDER DISTRIBUTION")
print("-" * 40)
total_gender = sum(gender_counts.values())
for gender, count in gender_counts.most_common():
    pct = (count / total_gender) * 100
    print(f"{gender}: {count} ({pct:.1f}%)")
print()

# Occupation distribution
occupation_counts = Counter([p.occupation for p in generated_personas])
top_occupations = occupation_counts.most_common(5)
print("💼 TOP OCCUPATIONS")
print("-" * 40)
for occupation, count in top_occupations:
    pct = (count / len(generated_personas)) * 100
    print(f"• {occupation}: {count} ({pct:.1f}%)")
print()

# Education distribution
education_counts = Counter([p.education for p in generated_personas if p.education])
print("🎓 EDUCATION LEVELS")
print("-" * 40)
if education_counts:
    for edu, count in education_counts.most_common(3):
        pct = (count / len([p for p in generated_personas if p.education])) * 100
        print(f"• {edu}: {count} ({pct:.1f}%)")
else:
    print("Not specified")
print()

# Location distribution
location_counts = Counter([p.location for p in generated_personas if p.location])
print("📍 TOP LOCATIONS")
print("-" * 40)
if location_counts:
    for location, count in location_counts.most_common(3):
        pct = (count / len([p for p in generated_personas if p.location])) * 100
        print(f"• {location}: {count} ({pct:.1f}%)")
print()

print("=" * 80)
print("✅ This demographic summary will appear in the UI after generation!")
print("=" * 80)
print()
print("Features:")
print("• Age statistics with mean, min, max, and age group distribution")
print("• Gender breakdown with percentages")
print("• Top 5 occupations with percentages")
print("• Education level distribution")
print("• Geographic location distribution")
print("• Visual display in 3-column layout in Streamlit")
print()
print("=" * 80)
