#!/usr/bin/env python3
"""
Visual Example: AI Survey Parser with Question Groups
======================================================

This script demonstrates how the enhanced AI Survey Parser handles
surveys with multiple question groups using different response formats.

Example: Mixed Survey with 3 Different Formats
"""

# Example survey text that would be pasted into the parser
EXAMPLE_SURVEY = """
Welcome to our Customer Satisfaction Survey!

Please answer the following questions honestly. Your feedback helps us improve.

SECTION 1: Service Quality (Rate 1-5)
Rate each aspect where 1=Very Poor, 2=Poor, 3=Average, 4=Good, 5=Excellent

1. How would you rate the overall service quality?
2. How satisfied are you with response time?
3. Rate the professionalism of our staff.
4. How well did we meet your expectations?
5. Rate the ease of using our service.

SECTION 2: Specific Features (Yes/No)
Please answer Yes or No for each feature:

6. Did you use the mobile app?
7. Did you contact customer support?
8. Were you able to complete your task successfully?
9. Did you encounter any technical issues?
10. Would you recommend us to a friend?

SECTION 3: Open Feedback
Please provide detailed responses:

11. What did you like most about your experience?
12. What areas need improvement?
13. Any additional comments or suggestions?
"""

# Expected AI parser output structure
EXPECTED_OUTPUT = {
    "instructions": "Welcome to our Customer Satisfaction Survey! Please answer the following questions honestly. Your feedback helps us improve.",
    "question_groups": [
        {
            "group_name": "Service Quality Ratings",
            "format_type": "scale",
            "format_details": {
                "min": 1,
                "max": 5,
                "labels": {
                    "1": "Very Poor",
                    "2": "Poor",
                    "3": "Average",
                    "4": "Good",
                    "5": "Excellent"
                },
                "description": "1-5 scale where 1=Very Poor and 5=Excellent"
            },
            "questions": [
                "How would you rate the overall service quality?",
                "How satisfied are you with response time?",
                "Rate the professionalism of our staff.",
                "How well did we meet your expectations?",
                "Rate the ease of using our service."
            ]
        },
        {
            "group_name": "Feature Usage Questions",
            "format_type": "yes_no",
            "format_details": {
                "description": "Binary Yes/No responses"
            },
            "questions": [
                "Did you use the mobile app?",
                "Did you contact customer support?",
                "Were you able to complete your task successfully?",
                "Did you encounter any technical issues?",
                "Would you recommend us to a friend?"
            ]
        },
        {
            "group_name": "Open Feedback",
            "format_type": "text",
            "format_details": {
                "description": "Free text responses with detailed feedback"
            },
            "questions": [
                "What did you like most about your experience?",
                "What areas need improvement?",
                "Any additional comments or suggestions?"
            ]
        }
    ]
}

# Generated validation rules (stored as list, one per question)
VALIDATION_RULES = [
    # Q1-Q5: Scale validation
    {"type": "number", "min": 1, "max": 5, "instruction": "You MUST respond with ONLY a single number between 1 and 5. No explanation."},
    {"type": "number", "min": 1, "max": 5, "instruction": "You MUST respond with ONLY a single number between 1 and 5. No explanation."},
    {"type": "number", "min": 1, "max": 5, "instruction": "You MUST respond with ONLY a single number between 1 and 5. No explanation."},
    {"type": "number", "min": 1, "max": 5, "instruction": "You MUST respond with ONLY a single number between 1 and 5. No explanation."},
    {"type": "number", "min": 1, "max": 5, "instruction": "You MUST respond with ONLY a single number between 1 and 5. No explanation."},
    
    # Q6-Q10: Yes/No validation
    {"type": "word", "allowed": ["Yes", "No"], "instruction": "You MUST respond with ONLY 'Yes' or 'No'. No explanation."},
    {"type": "word", "allowed": ["Yes", "No"], "instruction": "You MUST respond with ONLY 'Yes' or 'No'. No explanation."},
    {"type": "word", "allowed": ["Yes", "No"], "instruction": "You MUST respond with ONLY 'Yes' or 'No'. No explanation."},
    {"type": "word", "allowed": ["Yes", "No"], "instruction": "You MUST respond with ONLY 'Yes' or 'No'. No explanation."},
    {"type": "word", "allowed": ["Yes", "No"], "instruction": "You MUST respond with ONLY 'Yes' or 'No'. No explanation."},
    
    # Q11-Q13: No validation (free text)
    None,
    None,
    None
]

def print_visual_representation():
    """Print a visual representation of how the UI displays the groups."""
    print("=" * 80)
    print("AI SURVEY PARSER - QUESTION GROUPS")
    print("=" * 80)
    print()
    
    print("📋 Instructions:")
    print(EXPECTED_OUTPUT["instructions"])
    print()
    
    print("─" * 80)
    print(f"Found {len(EXPECTED_OUTPUT['question_groups'])} question groups")
    print("─" * 80)
    print()
    
    question_counter = 1
    
    for group_idx, group in enumerate(EXPECTED_OUTPUT["question_groups"], 1):
        print(f"📌 GROUP {group_idx}: {group['group_name']}")
        print(f"   Format: {group['format_type']}")
        print(f"   Description: {group['format_details'].get('description', 'N/A')}")
        print(f"   Questions: {len(group['questions'])}")
        print()
        
        for question in group["questions"]:
            validation = VALIDATION_RULES[question_counter - 1]
            print(f"   Q{question_counter}: {question}")
            if validation:
                if validation["type"] == "number":
                    print(f"            ✓ Validation: Number ({validation['min']}-{validation['max']})")
                elif validation["type"] == "word":
                    print(f"            ✓ Validation: {', '.join(validation['allowed'])}")
            else:
                print(f"            ○ No validation (free text)")
            question_counter += 1
        print()
    
    print("─" * 80)
    print(f"Total: {question_counter - 1} questions across {len(EXPECTED_OUTPUT['question_groups'])} groups")
    print("=" * 80)

def show_simulation_flow():
    """Show how questions are processed during simulation."""
    print("\n\n")
    print("=" * 80)
    print("SIMULATION FLOW")
    print("=" * 80)
    print()
    
    print("When running simulation with 2 personas:")
    print()
    
    personas = ["Alice (35F, Teacher)", "Bob (42M, Engineer)"]
    
    for persona_idx, persona in enumerate(personas, 1):
        print(f"🧑 Persona {persona_idx}: {persona}")
        print("─" * 40)
        
        question_idx = 0
        for group_idx, group in enumerate(EXPECTED_OUTPUT["question_groups"], 1):
            print(f"  📌 {group['group_name']}:")
            
            for q in group["questions"][:2]:  # Show first 2 questions per group
                validation = VALIDATION_RULES[question_idx]
                print(f"     Q{question_idx + 1}: {q[:50]}...")
                
                if validation and validation.get("type") == "number":
                    print(f"        → LLM receives: Format = Number ({validation['min']}-{validation['max']})")
                    print(f"        ← Response: {validation['min'] + persona_idx}")  # Example response
                elif validation and validation.get("type") == "word":
                    response = validation["allowed"][persona_idx % 2]
                    print(f"        → LLM receives: Format = {'/'.join(validation['allowed'])}")
                    print(f"        ← Response: {response}")
                else:
                    print(f"        → LLM receives: No strict format")
                    print(f"        ← Response: [Detailed text response...]")
                
                question_idx += 1
            
            if len(group["questions"]) > 2:
                remaining = len(group["questions"]) - 2
                print(f"     ... ({remaining} more questions in this group)")
                question_idx += remaining
            print()
        print()

def show_benefits():
    """Show the benefits of grouped validation."""
    print("=" * 80)
    print("KEY BENEFITS")
    print("=" * 80)
    print()
    
    benefits = [
        ("✓ Flexibility", "Handle surveys with multiple response types in one configuration"),
        ("✓ Accuracy", "Each question gets appropriate validation, reducing errors"),
        ("✓ Organization", "Clear visual grouping makes large surveys manageable"),
        ("✓ Smart Detection", "AI automatically identifies groups and formats"),
        ("✓ Easy Editing", "Edit min/max values, word lists, or formats per group"),
        ("✓ Data Quality", "Enforced formats produce clean, analyzable data")
    ]
    
    for benefit, description in benefits:
        print(f"{benefit:<20} {description}")
    print()
    
    print("─" * 80)
    print("Example Use Cases:")
    print("─" * 80)
    print()
    print("1. Customer Satisfaction Surveys")
    print("   - NPS scores (0-10) + Feature ratings (1-5) + Open feedback")
    print()
    print("2. Health Assessments")
    print("   - Symptom presence (Yes/No) + Severity scales (0-10) + Descriptions")
    print()
    print("3. Research Questionnaires")
    print("   - Demographics (text) + Likert scales + Binary choices + Open-ended")
    print()
    print("4. Product Feedback")
    print("   - Overall rating (1-5) + Feature checkboxes + Improvement suggestions")
    print()

if __name__ == "__main__":
    print("\n")
    print("🚀 AI Survey Parser with Question Groups - Visual Example")
    print()
    
    print_visual_representation()
    show_simulation_flow()
    show_benefits()
    
    print("=" * 80)
    print("📖 For full documentation, see: docs/AI_SURVEY_PARSER_GROUPS.md")
    print("=" * 80)
    print()
