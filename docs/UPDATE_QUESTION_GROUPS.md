# Enhanced AI Survey Parser - Update Log

## 🎉 New Feature: Question Groups with Per-Group Validation

### Date: October 31, 2025

### Overview
The AI Survey Parser has been significantly enhanced to support **intelligent question grouping** with different response formats for each group.

### What's New

#### 1. Smart Group Detection
- AI automatically identifies distinct question groups in your survey
- Detects different response formats (scales, yes/no, text, etc.)
- Extracts scale ranges and labels from survey text

#### 2. Per-Group Response Validation
Each question group can have its own validation rules:
- **Number Scales**: Customizable min/max (e.g., 0-3, 1-5, 1-10)
- **Yes/No**: Binary validation
- **Word Lists**: Specific allowed words
- **Free Text**: No validation constraints

#### 3. Visual Organization
- Questions displayed in expandable groups
- Clear format indicators per group
- Easy editing within each group
- Total question count across all groups

### Files Modified

#### UI Changes (`pages/2_Simulation.py`)
- **Lines 500-540**: Enhanced AI parser prompt to detect question groups
- **Lines 545-780**: New grouped display with per-group validation controls
- **Lines 816-840**: Support for both grouped and flat validation formats

#### Backend Changes (`src/simulation.py`)
- **Line 100**: Added `per_question_validation` parameter to `run_survey()`
- **Line 873**: Added `per_question_validation` parameter to `run_survey_parallel()`
- **Lines 157-166, 910-920**: Logic to apply per-question validation rules

### Usage Example

**Input:** Mixed survey with different sections
```
Part 1: Rate 1-5
Q1-Q5: Likert scale questions

Part 2: Yes/No
Q6-Q10: Binary questions

Part 3: Feedback
Q11-Q13: Open text
```

**Output:** 3 groups with automatic validation
- Group 1: 5 questions with 1-5 number validation
- Group 2: 5 questions with Yes/No validation  
- Group 3: 3 questions with no validation (free text)

### Benefits

1. **Flexibility**: Handle complex surveys with mixed question types
2. **Accuracy**: Each question enforces its appropriate format
3. **Organization**: Large surveys remain manageable
4. **Smart Defaults**: AI auto-detects most formats correctly
5. **Easy Editing**: Modify validation rules per group
6. **Clean Data**: Format enforcement produces analyzable results

### Backward Compatibility

✅ **Fully backward compatible**
- Old flat format still supported
- Single validation for all questions still works
- No breaking changes to existing surveys
- Templates continue working as before

### Documentation

- **Full Guide**: `docs/AI_SURVEY_PARSER_GROUPS.md`
- **Visual Example**: `docs/VISUAL_EXAMPLE_GROUPS.py`
- Run example: `python3 docs/VISUAL_EXAMPLE_GROUPS.py`

### Next Steps

To use this feature:
1. Go to **Simulation** → **Survey** → **AI-Powered Survey Parser**
2. Paste your multi-section survey
3. Click **Parse with AI**
4. Review detected groups and validation
5. Edit as needed
6. Run simulation!

### Technical Details

**Data Structure:**
```python
{
    "instructions": "survey instructions",
    "question_groups": [
        {
            "group_name": "Group name",
            "format_type": "scale|yes_no|text|...",
            "format_details": {...},
            "questions": [...]
        }
    ]
}
```

**Session State:**
- `ai_parsed_questions`: Flat list of all questions
- `ai_parsed_validations`: List of validation rules (one per question)
- `ai_parsed_instructions`: Overall instructions

**Simulation:**
- Uses `per_question_validation` parameter
- Maps question index → validation rules
- LLM receives format-specific instructions per question

---

**Questions?** Check the documentation or run the visual example script!
