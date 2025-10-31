# AI Survey Parser with Question Groups

## Overview
The enhanced AI Survey Parser can now intelligently detect and manage **multiple question groups** with different response formats in a single survey. This is perfect for complex surveys that mix different types of questions (e.g., Likert scales, yes/no questions, open-ended questions).

## Key Features

### 1. **Automatic Group Detection**
The AI parser automatically identifies:
- Different response formats used in the survey
- Logical groupings of questions (e.g., Q1-Q5 use 5-point scale, Q6-Q10 are yes/no)
- Scale ranges and labels for each group

### 2. **Per-Group Response Validation**
Each question group can have its own validation rules:
- **Number Scales**: Define min/max values (e.g., 0-3, 1-5)
- **Yes/No Questions**: Binary validation
- **Word Lists**: Specific allowed words (e.g., "agree", "disagree", "neutral")
- **Free Text**: No strict validation

### 3. **Visual Group Organization**
Questions are displayed in expandable groups showing:
- Group name and description
- Number of questions in the group
- Detected or configured response format
- Editable questions within each group

## Usage Example

### Input Survey Text
```
Please answer the following questions about your recent experience.

Part 1: Rate your agreement (1-5 scale where 1=Strongly Disagree, 5=Strongly Agree)
1. The service met my expectations.
2. The staff was helpful and friendly.
3. I would recommend this to others.

Part 2: Yes/No Questions
4. Did you experience any issues?
5. Would you use our service again?
6. Did you receive a follow-up email?

Part 3: Open-ended Feedback
7. What did you like most about your experience?
8. What could we improve?
```

### AI Parser Output
The parser will create **3 groups**:

#### 📌 Group 1: Agreement Scale (3 questions)
- **Format**: `scale` (1-5)
- **Validation**: Numbers between 1 and 5
- Questions:
  - Q1: The service met my expectations.
  - Q2: The staff was helpful and friendly.
  - Q3: I would recommend this to others.

#### 📌 Group 2: Binary Responses (3 questions)
- **Format**: `yes_no`
- **Validation**: Only "Yes" or "No"
- Questions:
  - Q4: Did you experience any issues?
  - Q5: Would you use our service again?
  - Q6: Did you receive a follow-up email?

#### 📌 Group 3: Open Feedback (2 questions)
- **Format**: `text`
- **Validation**: None (free text)
- Questions:
  - Q7: What did you like most about your experience?
  - Q8: What could we improve?

## How It Works

### 1. Parse Survey
1. Navigate to **Simulation** page → **Survey** mode → **AI-Powered Survey Parser** tab
2. Paste your complete survey text (including all sections)
3. Click **"🔍 Parse with AI"**

### 2. Review Groups
The parser displays all detected groups with:
- Expandable sections for each group
- Detected response format and scale ranges
- All questions in that group

### 3. Configure Validation
For each group, you can:
- Enable/disable strict format enforcement
- Edit scale min/max values
- Modify allowed word lists
- Add custom validation rules

### 4. Run Simulation
- All questions across all groups are automatically numbered (Q1, Q2, Q3...)
- Each question uses its group's validation rules
- LLM receives appropriate format instructions per question

## Advanced Features

### Editing Questions
- Click any question text to edit it
- Questions maintain their group membership
- All edits are preserved when running simulation

### Custom Formats
If the AI doesn't detect the format correctly, you can manually select:
- **Number Range**: Set custom min/max values
- **Yes/No**: Binary responses
- **Word List**: Comma-separated allowed words
- **Free Text**: No validation

### Mixed Format Surveys
Perfect for:
- Customer satisfaction surveys (mix of scales and open feedback)
- Health assessments (symptoms yes/no + severity scales)
- Research questionnaires (demographics + Likert scales + open questions)
- Product feedback (ratings + specific features + suggestions)

## Benefits

### 1. **Flexibility**
Handle surveys with multiple response types in one go

### 2. **Accuracy**
Each question gets appropriate validation, reducing parsing errors

### 3. **Organization**
Clear visual structure makes it easy to review and edit large surveys

### 4. **Smart Defaults**
AI auto-detects most common formats, reducing manual configuration

## Example Workflows

### Workflow 1: Health Survey
```
Demographics (Q1-Q5): Free text (name, age, location, etc.)
Symptoms (Q6-Q15): Yes/No binary questions
Severity (Q16-Q25): 0-10 pain scale
Quality of Life (Q26-Q30): 1-5 Likert scale
Comments (Q31-Q32): Open text feedback
```
→ Creates 5 groups with appropriate validations

### Workflow 2: Customer Feedback
```
NPS Score (Q1): 0-10 scale
Feature Ratings (Q2-Q8): 1-5 stars
Binary Usage (Q9-Q12): Yes/No
Improvement Ideas (Q13-Q14): Free text
```
→ Creates 4 groups, each with proper format enforcement

## Tips

1. **Clear Section Headers**: Use clear section titles in your survey text to help AI detect groups
2. **Consistent Formatting**: Keep similar questions together for better grouping
3. **Scale Labels**: Include scale labels (e.g., "1=Strongly Disagree") for accurate detection
4. **Review Results**: Always review the parsed groups before running simulation
5. **Test First**: Run with a small sample first to verify format validation works correctly

## Backward Compatibility

The system still supports:
- **Old format**: Single validation for all questions (if AI returns flat question list)
- **Manual entry**: You can still use the Quick Start templates or manual question entry
- **No validation**: You can disable format enforcement entirely

## Technical Details

### Data Structure
```python
{
    "instructions": "Overall survey instructions",
    "question_groups": [
        {
            "group_name": "Descriptive group name",
            "format_type": "scale|yes_no|text|number|single_word",
            "format_details": {
                "min": 1,
                "max": 5,
                "labels": {"1": "Strongly Disagree", "5": "Strongly Agree"},
                "description": "1-5 Likert scale"
            },
            "questions": ["Q1 text", "Q2 text", ...]
        },
        ...
    ]
}
```

### Storage
- `st.session_state.ai_parsed_questions`: Flat list of all questions
- `st.session_state.ai_parsed_validations`: List of validation dicts (one per question)
- `st.session_state.ai_parsed_instructions`: Overall survey instructions

### Simulation
- Questions are passed with `per_question_validation` parameter
- Each question index maps to its validation rules
- LLM receives format-specific instructions per question

---

**Need help?** Check the examples or paste your survey text to see the AI parser in action!
