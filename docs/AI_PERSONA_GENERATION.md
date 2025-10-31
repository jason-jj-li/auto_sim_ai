# AI-Powered Persona Generation Feature

## Overview
This new feature allows users to paste free-form text describing a target population, and the AI will automatically extract demographic information and generate personas based on it.

## How It Works

### 1. AI Demographic Extraction
- Users paste text describing their target population (e.g., research study descriptions, survey audiences, marketing segments)
- The LLM analyzes the text using a specialized prompt
- Extracts structured demographic data in JSON format

### 2. Persona Generation
- The extracted demographics are converted into statistical distributions
- Personas are generated using the same PersonaGenerator engine
- Each persona gets realistic names, occupations, traits, and values

### 3. Key Extracted Demographics
The AI can extract:
- Age or age range (e.g., "25-35", "18-24")
- Gender distribution
- Occupation/profession
- Education level
- Location/region
- Income range
- Marital status
- Number of children
- Ethnicity/race
- Health status
- Political affiliation
- Religion
- Interests and hobbies
- Core values
- Sample size

## Usage Instructions

### Step 1: Connect to LLM
1. Go to the **Home** page
2. Enter your LM Studio/DeepSeek/OpenAI API details
3. Click "Test Connection"
4. Verify connection is successful

### Step 2: Navigate to AI Extraction
1. Go to **Setup** page
2. Select **Generate Personas** tab
3. Select **AI-Powered Extraction** sub-tab

### Step 3: Extract & Generate
1. Paste your population description in the text area
2. Set the number of personas to generate (5-500)
3. Click "Extract Demographics & Generate Personas"
4. Review extracted demographics
5. View generated personas

### Step 4: Use or Save Personas
- Click "Continue to Simulation" to use immediately
- OR click "Save Permanently" to keep across sessions

## Example Inputs

### Example 1: Healthcare Workers
```
Nurses and healthcare workers, ages 28-55, primarily female (80%), 
working in urban hospitals. Most have bachelor's or associate degrees 
in nursing. They value patient care, work-life balance, and professional 
development. Common challenges include long hours and high stress.
```

### Example 2: Tech Professionals
```
Tech-savvy millennials aged 25-40, mixed gender, living in major 
metropolitan areas. Most have college degrees and work in white-collar 
professions with incomes between $60K-$120K. They value convenience, 
sustainability, and social responsibility. Heavy users of smartphones 
and social media.
```

### Example 3: College Students
```
College students aged 18-24 in California universities. The population 
is approximately 60% female and 40% male, mostly majoring in STEM fields. 
Most are from middle to upper-middle-class families with household 
incomes between $75K-$150K. They value education, career success, and 
work-life balance.
```

### Example 4: Senior Citizens
```
Retired adults aged 65-85, living independently in suburban areas. 
Mix of genders with slightly more females. Most have high school or 
college education. Fixed incomes from pensions and social security. 
Value family, health, tradition, and community. Interested in gardening, 
volunteering, and spending time with grandchildren.
```

## Technical Implementation

### Files Modified
1. **`src/persona_generator.py`**
   - Added `extract_demographics_with_ai()` static method
   - Added `generate_personas_from_ai_extraction()` static method
   - Handles AI prompt generation, JSON parsing, and distribution creation

2. **`pages/1_Setup.py`**
   - Added new sub-tab "AI-Powered Extraction" under "Generate Personas"
   - Created UI with text input, extraction button, and results display
   - Integrated with existing persona management system

### Key Functions

#### `extract_demographics_with_ai(text_input, llm_client, model)`
- Takes free-form text input
- Sends specialized prompt to LLM
- Parses JSON response
- Returns structured demographic data

#### `generate_personas_from_ai_extraction(extracted_data, n, seed)`
- Takes extracted demographic data
- Creates statistical distributions for each attribute
- Generates n personas with the specified characteristics
- Returns list of persona dictionaries

### AI Prompt Design
The prompt instructs the LLM to:
- Extract specific demographic fields
- Return ONLY valid JSON
- Use null for missing fields
- Provide example output format
- Use low temperature (0.3) for consistent extraction

## Benefits

1. **Speed**: Generate personas from text in seconds
2. **Accuracy**: AI extracts nuanced demographic details
3. **Flexibility**: Works with any text description
4. **Natural**: No need to understand statistical distributions
5. **Comprehensive**: Captures both numeric and categorical attributes

## Limitations

1. Requires active LLM connection
2. Quality depends on LLM capabilities
3. May need multiple attempts for complex descriptions
4. JSON parsing can fail if LLM response is malformed

## Future Enhancements

- [ ] Support for uploading research papers/PDFs
- [ ] Multi-language support for input text
- [ ] Ability to refine/edit extracted demographics before generation
- [ ] Save extraction templates for reuse
- [ ] Batch processing multiple text descriptions
- [ ] Integration with external demographic databases

## Testing

Run the test script to verify installation:
```bash
python3 test_ai_extraction.py
```

Then test in the UI:
```bash
streamlit run app.py
```

## Troubleshooting

**Issue**: "LLM not connected" warning
- **Solution**: Go to Home page and connect to LLM first

**Issue**: "Failed to parse AI response as JSON"
- **Solution**: Try again with clearer text, or check LLM logs

**Issue**: Extracted demographics look incorrect
- **Solution**: Provide more specific details in your input text

**Issue**: Generated personas don't match description
- **Solution**: Review extracted demographics and regenerate with different seed

## License
Same as parent project

## Questions?
Please open an issue on GitHub with the tag "ai-extraction"
