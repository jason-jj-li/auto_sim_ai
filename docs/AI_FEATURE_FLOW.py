"""
AI-Powered Persona Generation - Visual Flow
=============================================

[User Input]
    |
    | Paste text description:
    | "College students aged 18-24 in California,
    |  60% female, 40% male, STEM majors,
    |  value education and work-life balance..."
    |
    v
[AI Extraction] 🧠
    |
    | LLM analyzes text with specialized prompt
    | Extracts structured demographic data
    |
    v
[Extracted Demographics] 📊
{
  "age_range": "18-24",
  "gender": "Mixed (60% female, 40% male)",
  "occupation": "College Students",
  "education": "Pursuing Bachelor's",
  "location": "California",
  "values": ["Education", "Work-life balance"],
  "interests": ["Technology", "Social media"]
}
    |
    | Convert to statistical distributions
    |
    v
[Persona Generation] 🎭
    |
    | PersonaGenerator.generate_personas_from_ai_extraction()
    | Creates N personas matching demographics
    |
    v
[Generated Personas] 👥

Persona 1: Sarah Chen
- Age: 21
- Gender: Female
- Occupation: Computer Science Student
- Location: University of California, Berkeley
- Values: Education, Career success, Innovation
- Traits: Analytical, Ambitious, Tech-savvy

Persona 2: Michael Rodriguez
- Age: 19
- Gender: Male
- Occupation: Engineering Student
- Location: Stanford University, California
- Values: Education, Work-life balance, Achievement
- Traits: Curious, Practical, Organized

... (48 more personas)

    |
    v
[User Action] ⚡
    |
    +-- Save Permanently → Disk storage (data/personas/)
    |
    +-- Continue to Simulation → Immediate use
    |
    +-- Review/Edit → View all personas

=============================================
Key Advantages:
=============================================

✅ Natural Language Input
   Just describe your population in plain text
   
✅ Intelligent Extraction
   AI understands context and nuances
   
✅ Automatic Distribution Creation
   Converts text to statistical models
   
✅ Realistic Personas
   Names, backgrounds, traits match demographics
   
✅ Instant Results
   Seconds from text to personas

=============================================
Technical Flow:
=============================================

1. UI Layer (1_Setup.py)
   - Text input area
   - Button trigger
   - Results display

2. Extraction Layer (persona_generator.py)
   - extract_demographics_with_ai()
   - Sends prompt to LLM
   - Parses JSON response

3. Generation Layer (persona_generator.py)
   - generate_personas_from_ai_extraction()
   - Creates distributions
   - Generates personas

4. Storage Layer
   - Session state (temporary)
   - Disk storage (permanent)
   - Both accessible in simulations

=============================================
"""

if __name__ == "__main__":
    print(__doc__)
