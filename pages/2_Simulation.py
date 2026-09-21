"""Simulation page for running surveys and interventions."""
import streamlit as st
import json
from datetime import datetime
from src import (
    PersonaManager, LMStudioClient, SimulationEngine, SimulationResult, ResultsStorage,
    SurveyTemplateLibrary, SurveyConfig, SurveyConfigManager,
    QuestionMetadata, SurveySection, render_navigation, render_page_header, section,
    render_stepper, render_empty_state,
    ABTestManager, Condition, ABTestConfig, run_ab_test,
    LongitudinalStudyEngine, WaveConfig, LongitudinalStudyConfig,
    LongitudinalStudyBuilder
)
from src.styles import apply_global_styles

st.set_page_config(page_title="Simulation - LLM Simulation", page_icon="A", layout="wide", initial_sidebar_state="collapsed")

# Apply global design system
apply_global_styles()

# Top Navigation
render_navigation(current_page="simulation")

render_page_header(
    "Simulation studio",
    "Design and run surveys, message tests, randomized comparisons, and longitudinal studies.",
    eyebrow="Experiment workspace",
)

# Initialize session state
if 'persona_manager' not in st.session_state:
    st.session_state.persona_manager = PersonaManager()
if 'results_storage' not in st.session_state:
    st.session_state.results_storage = ResultsStorage()
if 'llm_client' not in st.session_state:
    st.session_state.llm_client = None
if 'default_temperature' not in st.session_state:
    st.session_state.default_temperature = 0.1  # Lower for structured responses
if 'default_max_tokens' not in st.session_state:
    st.session_state.default_max_tokens = 500
if 'current_survey_config' not in st.session_state:
    st.session_state.current_survey_config = None
if 'survey_config_manager' not in st.session_state:
    st.session_state.survey_config_manager = SurveyConfigManager()

# Soft gates — the page always renders fully so modes are explorable;
# only the Run button is gated (ready_to_run below).
llm_ready = st.session_state.llm_client is not None

# Load personas: disk personas (permanent) + session personas (temporary from CSV uploads) + generated personas
disk_personas = st.session_state.persona_manager.load_all_personas()
session_personas = st.session_state.session_personas if 'session_personas' in st.session_state else []
generated_personas = st.session_state.generated_personas if 'generated_personas' in st.session_state else []
personas = disk_personas + session_personas + generated_personas

# ---- Wizard shell ----
# Each step renders alone and persists its outputs to session_state, so
# later steps read state instead of re-rendering earlier steps.
st.session_state.setdefault('sim_step', 1)
st.session_state.setdefault('sim_mode', 'Survey')
step = st.session_state.sim_step

mode = st.session_state.sim_mode
_sel = st.session_state.get('sim_persona_names')
selected_personas = (
    [p for p in personas if p.persona_id in _sel or p.name in _sel]
    if _sel is not None else personas
)
questions = st.session_state.get('sim_questions', [])
intervention_text = st.session_state.get('sim_intervention', '')
conditions = st.session_state.get('sim_conditions', [])
waves_config = st.session_state.get('sim_waves', [])
response_validation = st.session_state.get('sim_respval', None)
response_validations = st.session_state.get('sim_respvals', None)  # per-question list (AI parser)
survey_context = ""
stratify_by = st.session_state.get('sim_stratify_by', 'None')
random_assignment = st.session_state.get('sim_random_assignment', True)
test_name = st.session_state.get('sim_test_name', 'Intervention Comparison Test')
study_name = st.session_state.get('sim_study_name', 'Longitudinal Behavior Change Study')
intervention_wave = st.session_state.get('sim_intervention_wave')

_step_titles = {1: "Select simulation mode", 2: "Select personas", 3: "Configure", 4: "Run"}
render_stepper(
    step,
    ["Study type", "Population", "Configuration", "Review & run"],
    context=f"{mode} · {len(selected_personas)} selected persona{'s' if len(selected_personas) != 1 else ''}",
)

if step == 1:
    # Simulation mode selection
    section("1 · Select simulation mode", first=True)

    MODE_HELP = {
        "Survey": "Ask questions directly — market research, opinion polls, needs assessment.",
        "Message Testing": "Present a message/intervention first, then ask follow-up questions about reactions.",
        "A/B Testing": "Randomly assign personas to 2-5 conditions with different materials, compare outcomes.",
        "Longitudinal Study": "Multi-wave tracking with conversation memory — pre/post intervention effects over time.",
    }
    mode = st.segmented_control(
        "Choose simulation type",
        list(MODE_HELP.keys()),
        default=st.session_state.sim_mode,
        key="sim_mode_seg",
    ) or "Survey"
    st.session_state.sim_mode = mode
    st.caption(MODE_HELP[mode])

elif step == 2:
    # Persona selection
    section("2 · Select personas", first=True)

    selected_personas = st.multiselect(
        "Choose personas to include:",
        personas,
        default=personas,
        format_func=lambda p: f"{p.name} ({p.age}, {p.occupation}) {'[Generated]' if p in generated_personas else '[Permanent]' if p in disk_personas else '[Temporary]'}",
        key="persona_select"
    )

    if not selected_personas:
        render_empty_state(
            "No population selected",
            "Select at least one persona here, or create a new population on Setup.",
            icon="○",
        )
        if st.button("Open population builder →", key="empty_setup_link"):
            st.switch_page("pages/1_Setup.py")

    # Show persona breakdown
    if len(personas) > 0:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Available", len(personas))
        with col2:
            st.metric("Permanent", len(disk_personas))
        with col3:
            st.metric("Generated", len(generated_personas))
        with col4:
            st.metric("Temporary", len(session_personas))

    st.session_state.sim_persona_names = [p.persona_id for p in selected_personas]

elif step == 3:
    # ============================================================================
    # SECTION 3: COMPREHENSIVE SURVEY CONFIGURATION
    # ============================================================================
    section("3 · Configure", first=True)

    if mode == "Survey":
        # Create tabs for different configuration methods
        config_tab1, config_tab2 = st.tabs([
            "Quick Start (Templates)",
            "AI-Powered Survey Parser"
        ])

        # ========================================================================
        # TAB 1: QUICK START WITH TEMPLATES
        # ========================================================================
        with config_tab1:
            st.markdown("### Standard Survey Templates")
            st.write("Select a validated psychological or health instrument to get started instantly.")

            template_names = SurveyTemplateLibrary.get_template_names()

            selected_template = st.selectbox(
                "Choose a template:",
                [""] + template_names,
                format_func=lambda x: "-- Select a template --" if x == "" else x,
                help="Pre-built validated survey instruments"
            )

            if selected_template:
                # Load the template
                templates = SurveyTemplateLibrary.get_all_templates()
                template = templates[selected_template]

                # Show template info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Questions", len(template.get_all_questions()))
                with col2:
                    st.metric("Est. Time", f"{template.estimated_minutes} min")
                with col3:
                    st.metric("Version", template.version)

                st.caption(f"**Description:** {template.description}")

                # Preview questions
                with st.expander("Preview Questions"):
                    questions_list = template.get_all_questions()
                    for i, q in enumerate(questions_list, 1):
                        reverse_marker = " (rev.)" if q.reverse_scored else ""
                        st.write(f"{i}. {q.text}{reverse_marker}")
                        if q.scale_labels:
                            labels_str = ', '.join([f'{k}={v}' for k, v in sorted(q.scale_labels.items())])
                            st.caption(f"   Scale: {q.scale_min}-{q.scale_max}: {labels_str}")

                with st.expander("Response format enforcement (optional)"):

                    enforce_format = st.checkbox(
                        "Enforce strict response format",
                        value=False,
                        key="template_enforce_format",
                        help="Force responses to follow a specific format (recommended for numeric scales)"
                    )

                    if enforce_format:
                        format_type = st.selectbox(
                            "Format Type:",
                            ["Single Number", "Single Word", "JSON Object"],
                            key="template_format_type",
                            help="Choose the response format"
                        )

                        if format_type == "Single Number":
                            col_x, col_y = st.columns(2)
                            with col_x:
                                min_val = st.number_input("Min Value", value=0, step=1, key="template_fmt_min")
                            with col_y:
                                max_val = st.number_input("Max Value", value=3, step=1, key="template_fmt_max")

                            st.session_state.template_response_validation = {
                                "type": "number",
                                "min": min_val,
                                "max": max_val,
                                "instruction": f"You MUST respond with ONLY a single number between {min_val} and {max_val}. No explanation, just the number."
                            }
                            st.caption(f"Responses will be enforced as numbers between {min_val}-{max_val}")

                        elif format_type == "Single Word":
                            allowed_words = st.text_input(
                                "Allowed words (comma-separated):",
                                placeholder="yes, no, maybe",
                                key="template_allowed_words"
                            )
                            if allowed_words:
                                words_list = [w.strip() for w in allowed_words.split(',')]
                                st.session_state.template_response_validation = {
                                    "type": "word",
                                    "allowed": words_list,
                                    "instruction": f"You MUST respond with ONLY one of these words: {', '.join(words_list)}. No explanation."
                                }
                                st.caption(f"Responses must be one of: {', '.join(words_list)}")

                        elif format_type == "JSON Object":
                            json_schema = st.text_area(
                                "JSON Schema (example):",
                                value='{"answer": "number", "confidence": "low|medium|high"}',
                                key="template_json_schema"
                            )
                            st.session_state.template_response_validation = {
                                "type": "json",
                                "schema": json_schema,
                                "instruction": f"You MUST respond with ONLY a valid JSON object matching this schema: {json_schema}. No additional text."
                            }
                            st.caption("Responses will be enforced as JSON objects")
                    else:
                        st.session_state.template_response_validation = None

                # Load button
                st.markdown("---")
                if st.button("Load This Template", type="primary", use_container_width=True):
                    # Create config from template
                    st.session_state.current_survey_config = SurveyConfig.from_template(template)
                    st.toast(f"Loaded {selected_template}! You can customize it or run the simulation directly.")
                    st.rerun()

        # ========================================================================
        # TAB 2: AI-POWERED SURVEY PARSER (SIMPLIFIED)
        # ========================================================================
        with config_tab2:
            st.markdown("### AI-Powered Survey Parser")
            st.caption("Paste your survey text below and let AI extract the instructions and questions automatically.")

            survey_text = st.text_area(
                "Paste Survey Text Here:",
                placeholder="Example:\n\nI am a PI of a health survey, thanks for your participation. I will ask about your feelings recently. Please respond using:\n0 = Rarely/none of the time\n1 = Some or a little of the time\n2 = Occasionally/moderate amount\n3 = Most/all of the time\n\n1. I felt sad or depressed.\n2. I had trouble sleeping.\n3. I felt hopeful about the future.\n...",
                height=300,
                help="Paste your complete survey text including instructions and questions"
            )

            col_parse, col_clear = st.columns([3, 1])

            with col_parse:
                parse_button = st.button("Parse with AI", type="primary", use_container_width=True, disabled=not llm_ready)

            with col_clear:
                if st.button("Clear", use_container_width=True):
                    st.session_state.parsed_survey = None
                    st.rerun()

            if parse_button and survey_text:
                with st.spinner("AI is analyzing your survey text..."):
                    try:
                        # Use LLM to parse the survey text with group detection
                        parse_prompt = f"""You are a survey analysis expert. Parse the following survey text and intelligently group questions by their response format.

Analyze the survey and:
1. Extract overall instructions/context
2. Identify distinct question groups (e.g., Likert scale questions, Yes/No questions, open-ended questions)
3. Detect the response format for each group (scale range, yes/no, text, etc.)

Survey Text:
{survey_text}

Respond in JSON format:
{{
    "instructions": "overall survey instructions",
    "question_groups": [
        {{
            "group_name": "descriptive name for this group",
            "format_type": "scale|yes_no|text|number|single_word",
            "format_details": {{
                "min": 0,
                "max": 3,
                "labels": {{"0": "Rarely", "1": "Sometimes", "2": "Often", "3": "Always"}},
                "description": "0-3 scale where 0=Rarely and 3=Always"
            }},
            "questions": ["Q1: question text", "Q2: question text", ...]
        }},
        ...
    ]
}}

If all questions use the same format, create one group. Otherwise, split into logical groups.
Only return the JSON, no additional text."""

                        response = st.session_state.llm_client.chat_completion(
                            messages=[{"role": "user", "content": parse_prompt}],
                            temperature=0.1,
                            max_tokens=3000
                        )

                        # Parse JSON response
                        import json
                        import re

                        # Extract JSON from response (handle markdown code blocks)
                        response_text = response.strip()
                        if "```json" in response_text:
                            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                            if json_match:
                                response_text = json_match.group(1)
                        elif "```" in response_text:
                            json_match = re.search(r'```\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                            if json_match:
                                response_text = json_match.group(1)

                        parsed_data = json.loads(response_text)

                        # Store in session state
                        st.session_state.parsed_survey = parsed_data
                        st.toast("Survey parsed successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Failed to parse survey: {str(e)}")
                        st.caption("Please ensure you're connected to an LLM (check Setup page) and the survey text is clear.")

            # Display parsed results if available
            if hasattr(st.session_state, 'parsed_survey') and st.session_state.parsed_survey:
                st.markdown("---")
                st.markdown("### Parsed Survey")

                parsed = st.session_state.parsed_survey

                # Editable instructions
                instructions = st.text_area(
                    "Instructions (editable):",
                    value=parsed.get("instructions", ""),
                    height=100
                )

                # Check if using new grouped format or old flat format
                if "question_groups" in parsed:
                    # NEW GROUPED FORMAT
                    st.markdown("---")
                    st.markdown("#### Question Groups")
                    st.caption(f"Found **{len(parsed['question_groups'])}** question groups with different response formats")

                    # Initialize storage
                    all_questions = []
                    all_validations = []

                    # Display each group
                    for group_idx, group in enumerate(parsed["question_groups"]):
                        with st.expander(f"**{group.get('group_name', f'Group {group_idx+1}')}** ({len(group.get('questions', []))} questions)", expanded=True):
                            # Group description
                            format_details = group.get('format_details', {})
                            format_type = group.get('format_type', 'unknown')

                            st.markdown(f"**Response Format:** `{format_type}`")
                            if format_details.get('description'):
                                st.caption(format_details['description'])

                            # Show detected format
                            if format_type == 'scale' and 'min' in format_details and 'max' in format_details:
                                st.caption(f"Scale: {format_details['min']} - {format_details['max']}")
                            elif format_type == 'yes_no':
                                st.caption("✓ Binary: Yes/No")

                            # Editable questions in this group
                            st.markdown("**Questions:**")
                            group_questions = []

                            for q_idx, question in enumerate(group.get('questions', [])):
                                q_text = st.text_input(
                                    f"Q{len(all_questions) + q_idx + 1}:",
                                    value=question,
                                    key=f"parsed_g{group_idx}_q{q_idx}"
                                )
                                if q_text:
                                    group_questions.append(q_text)

                            # Configure format for this group
                            st.markdown("**Response Validation:**")

                            enforce_group = st.checkbox(
                                "Enforce format for this group",
                                value=True,
                                key=f"enforce_g{group_idx}",
                                help="Apply strict validation to responses"
                            )

                            group_validation = None

                            if enforce_group:
                                # Auto-detect validation from parsed format
                                if format_type == 'scale' and 'min' in format_details and 'max' in format_details:
                                    # Use detected scale
                                    min_val = format_details['min']
                                    max_val = format_details['max']

                                    # Allow editing
                                    col_x, col_y = st.columns(2)
                                    with col_x:
                                        min_val = st.number_input("Min", value=int(min_val), key=f"min_g{group_idx}")
                                    with col_y:
                                        max_val = st.number_input("Max", value=int(max_val), key=f"max_g{group_idx}")

                                    group_validation = {
                                        "type": "number",
                                        "min": min_val,
                                        "max": max_val,
                                        "instruction": f"You MUST respond with ONLY a single number between {min_val} and {max_val}. No explanation."
                                    }
                                    st.caption(f"{min_val}-{max_val} scale")

                                elif format_type == 'yes_no':
                                    group_validation = {
                                        "type": "word",
                                        "allowed": ["Yes", "No"],
                                        "instruction": "You MUST respond with ONLY 'Yes' or 'No'. No explanation."
                                    }
                                    st.caption("Yes/No validation")

                                elif format_type == 'single_word':
                                    # Allow custom word list
                                    allowed = st.text_input(
                                        "Allowed words (comma-separated):",
                                        value=", ".join(format_details.get('allowed', [])),
                                        key=f"words_g{group_idx}"
                                    )
                                    if allowed:
                                        words_list = [w.strip() for w in allowed.split(',')]
                                        group_validation = {
                                            "type": "word",
                                            "allowed": words_list,
                                            "instruction": f"You MUST respond with ONLY one of: {', '.join(words_list)}. No explanation."
                                        }
                                        st.caption(f"Allowed: {', '.join(words_list)}")

                                else:
                                    # Manual format selection
                                    manual_format = st.selectbox(
                                        "Format Type:",
                                        ["Number Range", "Yes/No", "Word List", "Free Text"],
                                        key=f"manual_fmt_g{group_idx}"
                                    )

                                    if manual_format == "Number Range":
                                        col_a, col_b = st.columns(2)
                                        with col_a:
                                            m_min = st.number_input("Min", value=1, key=f"m_min_g{group_idx}")
                                        with col_b:
                                            m_max = st.number_input("Max", value=5, key=f"m_max_g{group_idx}")
                                        group_validation = {
                                            "type": "number",
                                            "min": m_min,
                                            "max": m_max,
                                            "instruction": f"You MUST respond with ONLY a number between {m_min} and {m_max}."
                                        }
                                    elif manual_format == "Yes/No":
                                        group_validation = {
                                            "type": "word",
                                            "allowed": ["Yes", "No"],
                                            "instruction": "You MUST respond with ONLY 'Yes' or 'No'."
                                        }
                                    elif manual_format == "Word List":
                                        words = st.text_input("Words (comma-separated):", key=f"m_words_g{group_idx}")
                                        if words:
                                            wlist = [w.strip() for w in words.split(',')]
                                            group_validation = {
                                                "type": "word",
                                                "allowed": wlist,
                                                "instruction": f"You MUST respond with one of: {', '.join(wlist)}."
                                            }

                            # Store questions and validation for this group
                            for q in group_questions:
                                all_questions.append(q)
                                all_validations.append(group_validation)

                    # Store aggregated data
                    st.session_state.ai_parsed_questions = all_questions
                    st.session_state.ai_parsed_instructions = instructions
                    st.session_state.ai_parsed_validations = all_validations  # List of validations per question

                    st.caption(f"Ready: {len(all_questions)} questions across {len(parsed['question_groups'])} groups")

                else:
                    # OLD FLAT FORMAT (backward compatibility)
                    st.markdown("**Questions (editable):**")
                    question_texts = []

                    for i, question in enumerate(parsed.get("questions", []), 1):
                        q_text = st.text_input(
                            f"Q{i}:",
                            value=question,
                            key=f"parsed_q_{i}"
                        )
                        if q_text:
                            question_texts.append(q_text)

                    # Single validation for all
                    enforce_format = st.checkbox("Enforce strict response format", value=False, key="ai_parsed_enforce_format")
                    response_validation = None

                    if enforce_format:
                        format_type = st.selectbox("Format Type:", ["Single Number", "Single Word", "Yes/No", "Scale (1-5)"], key="ai_parsed_format_type")

                        if format_type == "Single Number":
                            col_x, col_y = st.columns(2)
                            with col_x:
                                min_val = st.number_input("Min Value", value=0, step=1, key="ai_fmt_min")
                            with col_y:
                                max_val = st.number_input("Max Value", value=3, step=1, key="ai_fmt_max")
                            response_validation = {
                                "type": "number",
                                "min": min_val,
                                "max": max_val,
                                "instruction": f"You MUST respond with ONLY a single number between {min_val} and {max_val}. No explanation, just the number."
                            }
                        elif format_type == "Yes/No":
                            response_validation = {
                                "type": "word",
                                "allowed": ["Yes", "No"],
                                "instruction": "You MUST respond with ONLY 'Yes' or 'No'. No explanation."
                            }
                        elif format_type == "Scale (1-5)":
                            response_validation = {
                                "type": "number",
                                "min": 1,
                                "max": 5,
                                "instruction": "You MUST respond with ONLY a single number between 1 and 5. No explanation, just the number."
                            }

                    st.session_state.ai_parsed_questions = question_texts
                    st.session_state.ai_parsed_instructions = instructions
                    st.session_state.ai_parsed_response_validation = response_validation

                    if question_texts:
                        st.caption(f"Ready to use: {len(question_texts)} questions")

        # ========================================================================
        # FINAL SURVEY SETUP (appears below all tabs)
        # ========================================================================
        st.markdown("---")
        st.markdown("### Current Survey Setup")

        # Determine which questions to use
        questions = []
        survey_context = ""

        if st.session_state.current_survey_config:
            # Use loaded config (from templates)
            config = st.session_state.current_survey_config
            questions = config.get_question_texts()
            survey_context = config.instructions
            if config.pre_survey_text:
                survey_context = config.pre_survey_text + "\n\n" + survey_context

            st.caption(f"Using: **{config.title}** ({len(questions)} questions)")
        elif hasattr(st.session_state, 'ai_parsed_questions') and st.session_state.ai_parsed_questions:
            # Use AI-parsed questions from tab 2
            questions = st.session_state.ai_parsed_questions
            survey_context = st.session_state.ai_parsed_instructions if hasattr(st.session_state, 'ai_parsed_instructions') else ""
            st.caption(f"Using AI-parsed survey: {len(questions)} questions")
        else:
            st.caption("No survey configured. Please use one of the tabs above to configure your survey.")

        # Show preview if questions exist
        if questions:
            with st.expander("Preview Complete Survey"):
                if survey_context:
                    st.markdown("**Instructions:**")
                    st.caption(survey_context)
                    st.markdown("---")

                st.markdown("**Questions:**")
                for i, q in enumerate(questions, 1):
                    st.write(f"{i}. {q}")

        # Get response validation from template OR AI parsed settings
        response_validation = None  # Single validation for all questions (legacy)
        response_validations = None  # List of validations per question (new grouped format)

        if hasattr(st.session_state, 'template_response_validation') and st.session_state.template_response_validation:
            response_validation = st.session_state.template_response_validation
            # Show validation info
            if response_validation:
                st.caption(f"Response Format (from template): {response_validation.get('instruction', 'Custom validation enabled')}")
        elif hasattr(st.session_state, 'ai_parsed_validations') and st.session_state.ai_parsed_validations:
            # NEW: Per-question validations (grouped format)
            response_validations = st.session_state.ai_parsed_validations
            # Show summary
            unique_formats = set()
            for v in response_validations:
                if v:
                    if v.get('type') == 'number':
                        unique_formats.add(f"Number ({v.get('min')}-{v.get('max')})")
                    elif v.get('type') == 'word':
                        unique_formats.add(f"Word ({', '.join(v.get('allowed', [])[:3])}...)" if len(v.get('allowed', [])) > 3 else f"Word ({', '.join(v.get('allowed', []))})")
            if unique_formats:
                st.caption(f"Multiple Response Formats: {', '.join(unique_formats)}")
        elif hasattr(st.session_state, 'ai_parsed_response_validation') and st.session_state.ai_parsed_response_validation:
            # OLD: Single validation for all questions (backward compatibility)
            response_validation = st.session_state.ai_parsed_response_validation
            # Show validation info
            if response_validation:
                st.caption(f"Response Format (from AI parser): {response_validation.get('instruction', 'Custom validation enabled')}")

    elif mode == "Message Testing":
        st.write("**Message Testing Mode**: Present information/message, then ask follow-up questions about reactions")

        # Create tabs for intervention configuration
        interv_tab1, interv_tab2 = st.tabs([
            "Manual Entry",
            "AI-Powered Generator"
        ])

        # ========================================================================
        # INTERVENTION TAB 1: MANUAL ENTRY
        # ========================================================================
        with interv_tab1:
            st.markdown("### Enter Message/Intervention Manually")

            intervention_text = st.text_area(
                "Message/Intervention Text:",
                value=st.session_state.get('manual_intervention_text', ''),
                placeholder="Enter the message, information, or intervention you want to present to personas...",
                height=150,
                help="This will be presented to each persona before asking questions",
                key="manual_intervention_input"
            )

            questions_text = st.text_area(
                "Follow-up Questions (one per line):",
                value=st.session_state.get('manual_intervention_questions', ''),
                placeholder="How does this information affect your views?\nWhat concerns do you have about this?\nWould you support this initiative?",
                height=120,
                help="Questions to ask after presenting the intervention",
                key="manual_questions_input"
            )

            # Store for later use
            st.session_state.manual_intervention_text = intervention_text
            st.session_state.manual_intervention_questions = questions_text

            questions = [q.strip() for q in questions_text.split('\n') if q.strip()]

            if intervention_text and questions:
                st.caption(f"Message prepared with {len(questions)} follow-up question(s)")
            elif not intervention_text:
                st.caption("Please enter intervention text")
            elif not questions:
                st.caption("Please enter at least one follow-up question")

        # ========================================================================
        # INTERVENTION TAB 2: AI-POWERED GENERATOR
        # ========================================================================
        with interv_tab2:
            st.markdown("### AI-Powered Message Generator")
            st.caption("Describe your intervention scenario in natural language, and AI will generate the intervention text and follow-up questions!")

            intervention_description = st.text_area(
                "Describe Your Message/Intervention Scenario:",
                placeholder="Example:\n\nI want to test how people react to a new health policy proposal. The intervention should explain that the government is considering mandatory health screenings for adults over 40. It would be free and take 30 minutes. I want to know if people would support it, what concerns they have, and how it might affect their behavior.",
                height=200,
                help="Describe your intervention in natural language - AI will generate structured content"
            )

            col_gen, col_clear = st.columns([3, 1])

            with col_gen:
                generate_button = st.button("Generate Message", type="primary", use_container_width=True, disabled=not llm_ready)

            with col_clear:
                if st.button("Clear", key="clear_intervention", use_container_width=True):
                    st.session_state.parsed_intervention = None
                    st.rerun()

            if generate_button and intervention_description:
                with st.spinner("AI is generating your intervention..."):
                    try:
                        # Use LLM to generate intervention
                        generation_prompt = f"""You are an intervention design expert. Based on the following description, generate:
1. A clear, neutral intervention text (2-4 paragraphs) that presents the information/scenario
2. A list of 4-6 follow-up questions to assess reactions

Description:
{intervention_description}

Respond in JSON format:
{{
    "intervention_text": "Generated intervention text here (2-4 paragraphs)",
    "follow_up_questions": ["question 1", "question 2", "question 3", "question 4", "question 5", "question 6"]
}}

Guidelines:
- Keep intervention text neutral and informative
- Make it realistic and detailed enough to evaluate
- Follow-up questions should assess: support/opposition, concerns, behavioral intentions, trust, fairness perceptions
- Questions should be open-ended to allow varied responses
- Keep tone professional and unbiased

Only return the JSON, no additional text."""

                        response = st.session_state.llm_client.chat_completion(
                            messages=[{"role": "user", "content": generation_prompt}],
                            temperature=0.3,
                            max_tokens=1500
                        )

                        # Parse JSON response
                        import json
                        import re

                        # Extract JSON from response (handle markdown code blocks)
                        response_text = response.strip()
                        if "```json" in response_text:
                            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                            if json_match:
                                response_text = json_match.group(1)
                        elif "```" in response_text:
                            json_match = re.search(r'```\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                            if json_match:
                                response_text = json_match.group(1)

                        parsed_data = json.loads(response_text)

                        # Store in session state
                        st.session_state.parsed_intervention = parsed_data
                        st.toast("Message generated successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Failed to generate intervention: {str(e)}")
                        st.caption("Please ensure you're connected to an LLM (check Setup page) and try again.")

            # Display generated results if available
            if hasattr(st.session_state, 'parsed_intervention') and st.session_state.parsed_intervention:
                st.markdown("---")
                st.markdown("### Generated Message")

                parsed = st.session_state.parsed_intervention

                # Editable intervention text
                intervention_text = st.text_area(
                    "Message Text (editable):",
                    value=parsed.get("intervention_text", ""),
                    height=200,
                    key="ai_intervention_text_widget"
                )

                # Editable questions
                st.markdown("**Follow-up Questions (editable):**")
                questions = []

                for i, question in enumerate(parsed.get("follow_up_questions", []), 1):
                    q_text = st.text_input(
                        f"Q{i}:",
                        value=question,
                        key=f"ai_interv_q_{i}"
                    )
                    if q_text:
                        questions.append(q_text)

                # Add more questions button
                if st.button("Add Another Question", key="add_interv_question"):
                    st.session_state.parsed_intervention["follow_up_questions"].append("")
                    st.rerun()

                # Use these for simulation (store the edited values)
                if intervention_text and questions:
                    st.caption(f"Ready to use: Message + {len(questions)} questions")
            else:
                # Initialize empty if no AI-generated content
                intervention_text = ""
                questions = []

        # Determine which intervention to use
        if hasattr(st.session_state, 'parsed_intervention') and st.session_state.parsed_intervention:
            # Use AI-generated (get from widget state)
            intervention_text = st.session_state.get('ai_intervention_text_widget', '')
            questions = [st.session_state.get(f'ai_interv_q_{i}', '') for i in range(1, 10) if st.session_state.get(f'ai_interv_q_{i}', '')]
        elif hasattr(st.session_state, 'manual_intervention_text'):
            # Use manual entry
            intervention_text = st.session_state.manual_intervention_text
            questions = [q.strip() for q in st.session_state.manual_intervention_questions.split('\n') if q.strip()]
        else:
            intervention_text = ""
            questions = []

        survey_context = ""
        response_validation = None

    elif mode == "A/B Testing":
        st.write("**A/B Testing Mode**: Compare multiple intervention conditions")

        # Initialize A/B test manager
        if 'ab_test_manager' not in st.session_state:
            st.session_state.ab_test_manager = ABTestManager(seed=42)

        # A/B Test configuration
        st.markdown("**A/B Test Configuration**")

        col1, col2 = st.columns([1, 1])

        with col1:
            test_name = st.text_input(
                "Test Name:",
                value=st.session_state.get('sim_test_name', 'Intervention Comparison Test'),
                help="Name for this A/B test"
            )

            n_conditions = st.number_input(
                "Number of Conditions:",
                min_value=2,
                max_value=5,
                value=2,
                help="How many different conditions to compare"
            )

        with col2:
            stratify_by = st.selectbox(
                "Group Assignment By:",
                ["None", "Age Group", "Gender", "Education", "Occupation"],
                index=["None", "Age Group", "Gender", "Education", "Occupation"].index(
                    st.session_state.get('sim_stratify_by', 'None')
                ),
                help="Group personas by demographic characteristics"
            )

            random_assignment = st.checkbox(
                "Random Assignment",
                value=st.session_state.get('sim_random_assignment', True),
                help="Randomly assign personas to conditions"
            )

        st.markdown("---")

        # Create tabs for condition configuration
        condition_tab1, condition_tab2 = st.tabs([
            "Manual Entry",
            "AI-Powered Generator"
        ])

        # ========================================================================
        # CONDITION TAB 1: MANUAL ENTRY
        # ========================================================================
        with condition_tab1:
            st.markdown("**Define Conditions Manually**")

            conditions = []
            for i in range(n_conditions):
                with st.expander(f"Condition {i+1} (Group {chr(65+i)})"):
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        condition_name = st.text_input(
                            f"Condition {i+1} Name:",
                            value=f"Condition {chr(65+i)}",
                            key=f"condition_name_{i}"
                        )

                        allocation_weight = st.number_input(
                            "Allocation Weight:",
                            min_value=0.1,
                            max_value=2.0,
                            value=1.0,
                            step=0.1,
                            help="Relative size of this condition (1.0 = equal allocation)",
                            key=f"allocation_weight_{i}"
                        )

                    with col2:
                        intervention_text = st.text_area(
                            f"Intervention Text for Condition {i+1}:",
                            placeholder=f"Enter the intervention/message for condition {chr(65+i)}...",
                            height=100,
                            key=f"intervention_text_{i}"
                        )

                    if condition_name and intervention_text:
                        conditions.append(Condition(
                            condition_id=f"condition_{i}",
                            condition_name=condition_name,
                            intervention_text=intervention_text,
                            allocation_weight=allocation_weight
                        ))

        # ========================================================================
        # CONDITION TAB 2: AI ONE-CLICK GENERATOR
        # ========================================================================
        with condition_tab2:
            st.markdown("**AI One-Click Generator**")
            st.caption("Describe your A/B test in natural language, and AI will generate everything needed!")

            # Show examples
            with st.expander("Examples: What to write"):
                st.markdown("""
            **Example 1:**
            ```
            I want to test different health messaging about exercise.
            Create 2 conditions comparing fear-based vs hope-based appeals
            for young adults. Include follow-up questions about motivation
            and intention to exercise.
            ```

            **Example 2:**
            ```
            Compare 3 product description styles (formal, casual, technical)
            for a new software tool. Target audience is small business owners.
            Ask questions about clarity, appeal, and purchase intent.
            ```

            **Example 3:**
            ```
            Test climate change messaging with 2 conditions: one focusing
            on statistics and data, another on personal stories. For general
            public. Include questions on concern level and willingness to act.
            ```
            """)

            # Natural language input
            test_description = st.text_area(
                "Describe Your A/B Test:",
                placeholder="Example: I want to compare 2 messaging approaches about healthy eating - one emphasizing health benefits and another focusing on cost savings. Target audience is college students. Please create follow-up questions about attitudes and behavior intentions.",
                height=150,
                help="Describe: (1) What you're testing, (2) How many conditions, (3) What differs between them, (4) Target audience, (5) What questions to ask"
            )

            col1, col2 = st.columns(2)
            with col1:
                auto_num_conditions = st.checkbox(
                    "Auto-detect number of conditions",
                    value=True,
                    help="Let AI determine optimal number based on your description"
                )
            with col2:
                if not auto_num_conditions:
                    override_conditions = st.number_input(
                        "Force number of conditions:",
                        min_value=2,
                        max_value=5,
                        value=n_conditions
                    )
                else:
                    override_conditions = None

            # Generate everything with one click
            if st.button("Generate Complete A/B Test", type="primary", use_container_width=True, disabled=not llm_ready):
                if not test_description or len(test_description.strip()) < 20:
                    st.warning("Please provide a more detailed description (at least 20 characters)")
                else:
                    with st.spinner("AI is generating your complete A/B test setup..."):
                        try:
                            # Create comprehensive prompt
                            num_cond_instruction = f"exactly {override_conditions}" if not auto_num_conditions else "2-4 (determine optimal number)"

                            prompt = f"""
You are an expert A/B testing researcher. Based on the user's description, generate a COMPLETE A/B test setup.

**User's Description:**
{test_description}

**Instructions:**
1. Analyze the description and create {num_cond_instruction} distinct test conditions
2. Write complete intervention text for each condition (50-200 words each)
3. Generate 3-5 relevant follow-up questions to measure outcomes
4. Ensure all elements are coherent and aligned with the test goal

**Output Format (STRICT JSON):**
{{
  "test_name": "Brief descriptive name for this test",
  "conditions": [
    {{
      "name": "Condition A name (2-4 words)",
      "text": "Full intervention text/message for this condition (complete paragraph)"
    }},
    {{
      "name": "Condition B name",
      "text": "Full intervention text/message for this condition (complete paragraph)"
    }}
  ],
  "questions": [
    "Question 1 text here?",
    "Question 2 text here?",
    "Question 3 text here?"
  ],
  "target_audience": "Brief description of target audience"
}}

Generate the complete A/B test now in valid JSON format:
"""

                            # Call LLM
                            llm_client = st.session_state.llm_client
                            response = llm_client.chat_completion(
                                messages=[{"role": "user", "content": prompt}],
                                temperature=0.7,
                                max_tokens=2000
                            )

                            # Parse JSON response
                            import json
                            import re

                            # Extract JSON from response (handle code blocks)
                            json_match = re.search(r'\{[\s\S]*\}', response)
                            if json_match:
                                json_str = json_match.group(0)
                                ab_test_data = json.loads(json_str)

                                # Validate structure
                                if 'conditions' in ab_test_data and 'questions' in ab_test_data:
                                    # Store in session state
                                    st.session_state.ai_complete_test = ab_test_data

                                    # Create Condition objects
                                    ai_conditions = []
                                    for i, cond in enumerate(ab_test_data['conditions']):
                                        ai_conditions.append(Condition(
                                            condition_id=f"ai_condition_{i}",
                                            condition_name=cond['name'],
                                            intervention_text=cond['text'],
                                            allocation_weight=1.0
                                        ))

                                    st.session_state.ai_parsed_conditions = ai_conditions
                                    st.session_state.ai_generated_questions = ab_test_data['questions']

                                    st.caption(f"Generated complete A/B test: {ab_test_data.get('test_name', 'Unnamed Test')}")

                                    # Display preview
                                    st.markdown("---")
                                    st.markdown("**Generated Test Preview**")

                                    # Test info
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.metric("Test Name", ab_test_data.get('test_name', 'N/A'))
                                        st.metric("Conditions", len(ai_conditions))
                                    with col2:
                                        st.metric("Questions", len(ab_test_data['questions']))
                                        st.metric("Target", ab_test_data.get('target_audience', 'General'))

                                    # Show conditions
                                    st.markdown("**Test Conditions:**")
                                    for i, condition in enumerate(ai_conditions):
                                        with st.expander(f"{condition.condition_name}", expanded=True):
                                            st.write(condition.intervention_text)

                                    # Show questions
                                    st.markdown("**Follow-up Questions:**")
                                    for i, q in enumerate(ab_test_data['questions'], 1):
                                        st.write(f"{i}. {q}")

                                    st.caption("Scroll down to see assignment preview and start simulation!")

                                else:
                                    st.error("AI response missing required fields (conditions or questions)")
                                    st.text_area("Raw AI Response:", response, height=200)
                            else:
                                st.error("Could not parse JSON from AI response")
                                st.text_area("Raw AI Response:", response, height=200)

                        except json.JSONDecodeError as e:
                            st.error(f"JSON parsing failed: {str(e)}")
                            st.caption("Tip: Try rephrasing your description more clearly")
                            with st.expander("Show raw AI response"):
                                st.text_area("Raw Response:", response, height=200)

                        except Exception as e:
                            st.error(f"Generation failed: {str(e)}")
                            st.caption("Make sure you're connected to an LLM (check Setup page)")

            # Show AI-generated conditions if available
            if 'ai_parsed_conditions' in st.session_state and st.session_state.ai_parsed_conditions:
                st.markdown("---")
                st.markdown("**AI-Generated Test Ready**")
                st.caption("Your AI-generated A/B test is ready. You can modify conditions in the Manual Entry tab if needed.")

                # Option to clear and regenerate
                if st.button("Clear & Start Over", type="secondary"):
                    st.session_state.ai_parsed_conditions = []
                    st.session_state.ai_generated_questions = []
                    if 'ai_complete_test' in st.session_state:
                        del st.session_state.ai_complete_test
                    if 'ai_generated_conditions' in st.session_state:
                        del st.session_state.ai_generated_conditions
                    st.rerun()

        st.markdown("---")

        # Follow-up questions
        st.markdown("**Follow-up Questions**")
        st.caption("These questions will be asked to all participants after they receive their assigned condition.")

        # Pre-fill with AI-generated questions if available
        default_questions = ""
        if 'ai_generated_questions' in st.session_state and st.session_state.ai_generated_questions:
            default_questions = "\n".join(st.session_state.ai_generated_questions)
            st.caption(f"Using {len(st.session_state.ai_generated_questions)} AI-generated questions (you can edit them below)")

        questions_text = st.text_area(
            "Questions (one per line):",
            value=default_questions,
            placeholder="How does this information affect your views?\nWhat concerns do you have?\nWould you support this initiative?",
            height=120,
            help="Questions to ask after presenting the intervention"
        )

        questions = [q.strip() for q in questions_text.split('\n') if q.strip()]

        # Add per-question response format configuration
        if questions:
            st.markdown("---")
            st.markdown("**Response Format Requirements (Optional)**")
            st.caption("Configure specific response formats for each question. Leave blank for open-ended responses.")

            # Initialize session state for question validations
            if 'ab_question_validations' not in st.session_state:
                st.session_state.ab_question_validations = {}

            question_validations = {}

            with st.expander("Configure Response Formats", expanded=False):
                for i, question in enumerate(questions):
                    st.markdown(f"**Question {i+1}:** {question[:80]}{'...' if len(question) > 80 else ''}")

                    col1, col2 = st.columns([1, 2])

                    with col1:
                        format_type = st.selectbox(
                            f"Format type:",
                            ["Open-ended (detailed)", "Scale (0-3)", "Scale (1-5)", "Scale (1-7)", "Yes/No", "Custom"],
                            key=f"ab_format_type_{i}",
                            help="Select the expected response format"
                        )

                    with col2:
                        if format_type == "Open-ended (detailed)":
                            instruction = None  # No specific format, will use default detailed guidance
                            st.caption("Will encourage 2-4 sentence responses")

                        elif format_type == "Scale (0-3)":
                            instruction = "Answer with a single number: 0 (Not at all), 1 (Several days), 2 (More than half the days), or 3 (Nearly every day)"
                            st.caption("PHQ-9 / GAD-7 style scale")

                        elif format_type == "Scale (1-5)":
                            instruction = "Answer with a single number from 1 (Strongly Disagree) to 5 (Strongly Agree)"
                            st.caption("Likert scale")

                        elif format_type == "Scale (1-7)":
                            instruction = "Answer with a single number from 1 to 7, where 1 = lowest and 7 = highest"
                            st.caption("7-point scale")

                        elif format_type == "Yes/No":
                            instruction = "Answer with either 'Yes' or 'No' only"
                            st.caption("Binary choice")

                        elif format_type == "Custom":
                            instruction = st.text_input(
                                "Custom instruction:",
                                placeholder="e.g., Answer with a percentage between 0-100",
                                key=f"ab_custom_instruction_{i}"
                            )
                            if not instruction:
                                instruction = None

                    # Store validation for this question
                    if instruction:
                        validation = {'instruction': instruction, 'type': 'instruction'}
                        if format_type == "Scale (0-3)":
                            validation.update({'type': 'number', 'min': 0, 'max': 3})
                        elif format_type == "Scale (1-5)":
                            validation.update({'type': 'number', 'min': 1, 'max': 5})
                        elif format_type == "Scale (1-7)":
                            validation.update({'type': 'number', 'min': 1, 'max': 7})
                        elif format_type == "Yes/No":
                            validation.update({'type': 'word', 'allowed': ['Yes', 'No']})
                        question_validations[i] = validation

                    st.markdown("---")

            # Store in session state
            st.session_state.ab_question_validations = question_validations

            if question_validations:
                st.caption(f"{len(question_validations)} questions have specific format requirements")

        # Use AI-generated conditions if available, otherwise use manual conditions
        if 'ai_parsed_conditions' in st.session_state and st.session_state.ai_parsed_conditions:
            conditions = st.session_state.ai_parsed_conditions

        if len(conditions) >= 2 and questions:
            st.caption(f"A/B Test configured: {len(conditions)} conditions, {len(questions)} questions")

            # Show assignment preview
            if selected_personas:
                st.markdown("**Assignment Preview**")

                # Create test config
                test_config = ABTestConfig(
                    test_name=test_name,
                    conditions=conditions,
                    questions=questions,
                    random_assignment=random_assignment,
                    stratify_by=stratify_by.lower().replace(" ", "_") if stratify_by != "None" else None
                )

                preview_seed = int(st.session_state.get('sim_seed', 0)) or 42
                assignments = ABTestManager(seed=preview_seed).assign_personas(
                    personas=selected_personas,
                    conditions=conditions,
                    stratify_by=test_config.stratify_by,
                    random_assignment=random_assignment,
                )

                # Show assignment distribution
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Total Participants", len(selected_personas))

                with col2:
                    condition_counts = {}
                    for condition in conditions:
                        count = sum(1 for assignment in assignments.values() if assignment == condition.condition_id)
                        condition_counts[condition.condition_name] = count

                    st.metric("Conditions", len(conditions))

                with col3:
                    # Show most common assignment
                    if assignments:
                        most_common = max(set(assignments.values()), key=list(assignments.values()).count)
                        most_common_name = next(c.condition_name for c in conditions if c.condition_id == most_common)
                        st.metric("Largest Group", most_common_name)

                # Show detailed assignment
                with st.expander("Detailed Assignment"):
                    assignment_df = []
                    for persona_id, condition_id in assignments.items():
                        persona_obj = next((p for p in selected_personas if p.persona_id == persona_id), None)
                        if persona_obj:
                            condition_name = next(c.condition_name for c in conditions if c.condition_id == condition_id)
                            assignment_df.append({
                                "Persona": persona_obj.name,
                                "Age": persona_obj.age,
                                "Gender": persona_obj.gender,
                                "Condition": condition_name
                            })

                    if assignment_df:
                        import pandas as pd
                        df = pd.DataFrame(assignment_df)
                        st.dataframe(df, use_container_width=True)
        else:
            if len(conditions) < 2:
                st.caption("Please define at least 2 conditions")
            if not questions:
                st.caption("Please enter at least one follow-up question")

        # Store for simulation
        intervention_text = ""  # Not used in A/B testing
        survey_context = ""
        response_validation = None

    elif mode == "Longitudinal Study":
        st.write("**Longitudinal Study Mode**: Track changes across multiple time points with conversation memory")

        st.caption("""
    **How it works**: Personas remember all previous interactions. Each wave builds on previous responses,
    creating realistic behavior change patterns over time.
    """)

        # ========================================================================
        # LONGITUDINAL STUDY CONFIGURATION
        # ========================================================================
        st.markdown("**Study Design**")

        col1, col2 = st.columns([1, 1])

        with col1:
            study_name = st.text_input(
                "Study Name:",
                value=st.session_state.get('sim_study_name', 'Longitudinal Behavior Change Study'),
                help="Name for this longitudinal study"
            )

            n_waves = st.number_input(
                "Number of Waves (Time Points):",
                min_value=2,
                max_value=10,
                value=3,
                help="How many measurement waves (e.g., baseline, post-intervention, follow-up)"
            )

        with col2:
            study_type = st.selectbox(
                "Study Design:",
                ["Pre-Post (with Intervention)", "Repeated Measures (no intervention)", "Pre-Multiple Post"],
                help="Pre-Post: Baseline → Intervention → Follow-up | Repeated: Just track over time"
            )

            # Show design diagram
            if study_type == "Pre-Post (with Intervention)":
                st.caption("Wave 1 (Pre) → Intervention → Wave 2 (Post)")
            elif study_type == "Repeated Measures (no intervention)":
                st.caption("Wave 1 → Wave 2 → Wave 3 (natural progression)")
            else:
                st.caption("Wave 1 (Pre) → Intervention → Waves 2-N (Multiple follow-ups)")

        st.markdown("---")

        # ========================================================================
        # WAVE CONFIGURATION
        # ========================================================================
        st.markdown("**Configure Each Wave**")

        # Initialize waves storage
        if 'longitudinal_waves' not in st.session_state:
            st.session_state.longitudinal_waves = []

        waves_config = []

        for wave_idx in range(int(n_waves)):
            with st.expander(f"Wave {wave_idx + 1} Configuration", expanded=(wave_idx == 0)):
                col1, col2 = st.columns([1, 2])

                with col1:
                    wave_name = st.text_input(
                        f"Wave {wave_idx + 1} Name:",
                        value=f"Wave {wave_idx + 1}",
                        key=f"wave_name_{wave_idx}",
                        help="E.g., 'Baseline', 'Post-Intervention', '1-month Follow-up'"
                    )

                    time_description = st.text_input(
                        "Time Description:",
                        value=f"Day {wave_idx * 7}" if wave_idx > 0 else "Baseline",
                        key=f"wave_time_{wave_idx}",
                        help="E.g., 'Week 1', '1 month later', 'Immediately after'"
                    )

                with col2:
                    wave_questions = st.text_area(
                        f"Questions for Wave {wave_idx + 1}:",
                        placeholder="Enter questions (one per line)\nExample:\n- How is your stress level? (1-10)\n- How often do you exercise?",
                        height=100,
                        key=f"wave_questions_{wave_idx}",
                        help="Enter one question per line"
                    )

                # Parse questions
                questions_list = [q.strip() for q in wave_questions.split('\n') if q.strip() and not q.strip().startswith('#')]

                if questions_list:
                    waves_config.append({
                        'wave_id': wave_idx,
                        'name': wave_name,
                        'time_description': time_description,
                        'questions': questions_list
                    })

        st.markdown("---")

        # ========================================================================
        # INTERVENTION CONFIGURATION (if applicable)
        # ========================================================================
        intervention_text = ""
        intervention_wave = None

        if study_type != "Repeated Measures (no intervention)":
            st.markdown("**Intervention Configuration**")

            col1, col2 = st.columns([1, 2])

            with col1:
                intervention_wave = st.number_input(
                    "Apply Intervention After Wave:",
                    min_value=1,
                    max_value=int(n_waves) - 1,
                    value=min(
                        max(1, int(st.session_state.get('sim_intervention_wave') or 1)),
                        int(n_waves) - 1,
                    ),
                    help="Intervention will be shown after this wave"
                )

                st.caption(f"Timeline: Wave {intervention_wave} → Intervention → Wave {intervention_wave + 1}")

            with col2:
                intervention_text = st.text_area(
                    "Intervention Text:",
                    placeholder="Enter the intervention message or information to present...\n\nExample:\n'Research shows that practicing mindfulness meditation for 10 minutes daily can reduce stress by 30%. Try this simple breathing exercise...'",
                    height=150,
                    help="This will be shown to personas after the specified wave"
                )

        # Prepare longitudinal study configuration
        if waves_config:
            st.markdown("---")
            st.markdown("**Study Summary**")

            total_questions = sum(len(w['questions']) for w in waves_config)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Waves", len(waves_config))
            with col2:
                st.metric("Total Questions", total_questions)
            with col3:
                st.metric("Personas", len(selected_personas))
            with col4:
                total_responses = len(selected_personas) * total_questions
                st.metric("Total Responses", total_responses)

            # Show timeline visualization
            with st.expander("Study Timeline"):
                timeline_text = ""
                for i, wave in enumerate(waves_config):
                    timeline_text += f"**{wave['name']}** ({wave['time_description']})\n"
                    timeline_text += f"  - {len(wave['questions'])} questions\n"

                    # Add intervention marker
                    if intervention_wave and i == intervention_wave - 1:
                        timeline_text += f"\n**INTERVENTION APPLIED**\n"
                        if intervention_text:
                            preview = intervention_text[:100] + "..." if len(intervention_text) > 100 else intervention_text
                            timeline_text += f"  - {preview}\n"

                    timeline_text += "\n"

                st.markdown(timeline_text)

        # Store for simulation
        questions = []  # Will be handled differently for longitudinal
        survey_context = ""
        response_validation = None

    # Persist step-3 outputs for the Run step
    st.session_state.sim_questions = questions
    st.session_state.sim_intervention = intervention_text
    st.session_state.sim_conditions = conditions
    st.session_state.sim_waves = waves_config
    st.session_state.sim_respval = response_validation
    st.session_state.sim_respvals = response_validations
    if mode == "A/B Testing":
        st.session_state.sim_stratify_by = stratify_by
        st.session_state.sim_random_assignment = random_assignment
        st.session_state.sim_test_name = test_name
    if mode == "Longitudinal Study":
        st.session_state.sim_study_name = study_name
        st.session_state.sim_intervention_wave = intervention_wave

# ---- Shared validation — post-chain, so this pass's config edits count now ----
missing = []
if not llm_ready:
    missing.append("connect a model on Setup")
if not selected_personas:
    missing.append("select personas (step 2)")
if mode == "Survey":
    if not questions:
        missing.append("add questions (step 3)")
elif mode == "Message Testing":
    if not intervention_text:
        missing.append("write the message (step 3)")
    if not questions:
        missing.append("add follow-up questions (step 3)")
elif mode == "A/B Testing":
    if len(conditions) < 2:
        missing.append("define at least 2 conditions (step 3)")
    if not questions:
        missing.append("add questions (step 3)")
    if conditions and len(selected_personas) < len(conditions):
        missing.append("select at least one persona per condition (step 2)")
elif mode == "Longitudinal Study":
    if len(waves_config) < 2:
        missing.append("configure at least 2 waves (step 3)")
ready_to_run = not missing
_config_blockers = [m for m in missing if 'connect a model' not in m]

if step == 4:
    with st.container(border=True):
        section("Run", first=True)
        # Advanced settings (keep original)
        with st.expander("Advanced settings"):
            col1, col2 = st.columns(2)

            with col1:
                temperature = st.slider(
                    "Temperature",
                    min_value=0.0,
                    max_value=2.0,
                    value=st.session_state.default_temperature,
                    step=0.1,
                    help="Controls response randomness"
                )

            with col2:
                max_tokens = st.number_input(
                    "Max Tokens",
                    min_value=50,
                    max_value=None,  # no cap — type any value
                    value=st.session_state.default_max_tokens,
                    step=100,
                    help="Upper bound of the per-response token budget (not a target — chat models stop at their natural end). "
                         "Reasoning models (deepseek-reasoner/flash) spend thinking tokens out of this same budget: "
                         "if result rows show [Error: empty completion (finish_reason=length)], raise this (4000+)."
                )

            col3, col4 = st.columns(2)

            with col3:
                seed_input = st.number_input(
                    "Random Seed",
                    min_value=0,
                    value=int(st.session_state.get('sim_seed', 0)),
                    step=1,
                    help="0 = not fixed. A fixed seed makes LLM responses reproducible on providers that support it."
                )
                st.session_state.sim_seed = int(seed_input)
                seed = int(seed_input) or None

            with col4:
                verbalized_sampling = st.checkbox(
                    "Reduce Answer Collapse",
                    value=st.session_state.get('verbalized_sampling', False),
                    help="Verbalized sampling: the model first considers how people like this persona might "
                         "answer differently, then gives its own answer — counters mode collapse (arXiv:2607.18310)"
                )
                st.session_state.verbalized_sampling = verbalized_sampling

        # Initialize optimization variables with defaults
        enable_cache = True  # Always enable cache for better performance
        api_provider = st.session_state.get('api_provider', 'Local (LM Studio)')
        supports_parallel = api_provider in ["DeepSeek", "OpenAI", "Custom OpenAI-Compatible"]
        enable_parallel = supports_parallel and st.session_state.get('enable_parallel', False)
        max_workers = int(st.session_state.get('parallel_workers', 5)) if enable_parallel else 1

        # Run simulation
        if len(selected_personas) < 200:
            st.caption(f"{len(selected_personas)} personas selected — answer distributions get statistically stable at ~200+ synthetic respondents (Sun et al. 2024). Treat small-sample distributions as directional only.")

        # missing / ready_to_run computed in the wizard shell above

        if ready_to_run:
            if mode == "Longitudinal Study":
                total_queries = len(selected_personas) * sum(
                    len(wave.get('questions', [])) for wave in waves_config
                )
            else:
                total_queries = len(selected_personas) * len(questions)

            # Enhanced simulation estimation
            st.markdown("**Simulation plan**")

            # Estimate time and cost
            avg_time_per_call = 3 if enable_parallel else 5  # seconds
            estimated_time_seconds = (total_queries * avg_time_per_call) / (max_workers if enable_parallel else 1)
            estimated_minutes = estimated_time_seconds / 60

            # Rough cost estimation (varies by model)
            if api_provider == "Local (LM Studio)":
                cost_msg = "$0.00 (Local - Free)"
                cost_color = "green"
            elif api_provider == "DeepSeek":
                # DeepSeek: ~$0.00014 per 1K tokens (assume 500 tokens per call)
                estimated_cost = (total_queries * 500 / 1000) * 0.00014
                cost_msg = f"~${estimated_cost:.4f}"
                cost_color = "green"
            elif api_provider == "OpenAI":
                # OpenAI GPT-3.5: ~$0.002 per 1K tokens
                estimated_cost = (total_queries * 500 / 1000) * 0.002
                cost_msg = f"~${estimated_cost:.2f}"
                cost_color = "orange"
            else:
                cost_msg = "Varies by provider"
                cost_color = "gray"

            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("LLM Calls", f"{total_queries}")
            with col_b:
                st.metric("Est. Time", f"{estimated_minutes:.1f} min")
            with col_c:
                st.metric("Est. Cost", cost_msg)
            with col_d:
                parallel_status = "Parallel" if enable_parallel else "Sequential"
                st.metric("Mode", parallel_status)

            # Tips based on settings
            if total_queries > 100 and not enable_parallel:
                st.caption("**Tip:** Enable parallel processing for faster results with large simulations!")
            if total_queries > 50 and not enable_cache:
                st.caption("**Tip:** Enable caching to avoid re-running identical queries if you retry!")

            st.markdown("---")

            # Check if cloud API is being used
            # Parallel execution settings (for cloud APIs)
            if supports_parallel:
                col_p1, col_p2 = st.columns([1, 1])

                with col_p1:
                    enable_parallel = st.checkbox(
                        "Enable Parallel Execution",
                        value=st.session_state.get('enable_parallel', False),
                        help="Run multiple requests simultaneously for faster results (5-30x speedup)",
                        key="sim_enable_parallel"
                    )

                with col_p2:
                    if enable_parallel:
                        parallel_workers = st.number_input(
                            "Concurrent Workers",
                            min_value=1,
                            max_value=None,  # no cap — type any value
                            value=st.session_state.get('parallel_workers', 5),
                            step=1,
                            help="Requests in flight at once. DeepSeek's account-level concurrency cap is far above "
                                 "anything practical here (500+); the real bottleneck is provider latency. "
                                 "If rows show [Error: HTTP 429], dial this down.",
                            key="sim_parallel_workers"
                        )
                        # Update session state
                        st.session_state.parallel_workers = parallel_workers
                    else:
                        parallel_workers = 1

                # Update session state
                st.session_state.enable_parallel = enable_parallel

                # Show quick info
                if enable_parallel:
                    speedup = min(parallel_workers, 10)
                    st.caption(f"Parallel mode enabled with {parallel_workers} workers - Expected speedup: ~{speedup}x")

                st.markdown("---")
            else:
                # Local API - no parallel support
                st.session_state.enable_parallel = False
                st.session_state.parallel_workers = 1
                st.caption("Switch to a cloud API (DeepSeek/OpenAI) in the homepage to enable parallel execution")
                st.markdown("---")

            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                run_button = st.button("Run Simulation", type="primary", use_container_width=True)

            with col2:
                if 'simulation_running' in st.session_state and st.session_state.simulation_running:
                    if st.button("Stop", use_container_width=True, type="secondary"):
                        st.session_state.stop_simulation = True
                        st.session_state.simulation_running = False
                        st.caption("Stopping simulation... (may take a few seconds)")

            if run_button:
                st.session_state.simulation_running = True
                st.session_state.stop_simulation = False  # Reset stop flag

                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Real-time log window
                with st.expander("Live log", expanded=True):
                    log_area = st.empty()

                # Initialize log list
                if 'simulation_logs' not in st.session_state:
                    st.session_state.simulation_logs = []
                st.session_state.simulation_logs = []  # Clear previous logs

                def add_log(message: str, level: str = "INFO"):
                    """Add a log message with timestamp"""
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Include milliseconds

                    log_entry = f"[{timestamp}] [{level:8s}] {message}"
                    st.session_state.simulation_logs.append(log_entry)

                    # Show last 30 logs
                    log_area.code("\n".join(st.session_state.simulation_logs[-30:]))

                results_container = st.container()

                # Add initial log
                add_log("Simulation initialized", "SUCCESS")

                # Initialize cache if enabled
                cache = None
                if enable_cache:
                    from src import ResponseCache
                    cache = ResponseCache(strategy='hybrid', max_memory_entries=1000)
                    add_log("Response cache enabled (hybrid strategy)", "CACHE")
                    status_text.text("Cache enabled")

                # Create simulation engine
                engine = SimulationEngine(
                    st.session_state.llm_client,
                    cache=cache
                )

                add_log(f"Simulation engine initialized", "SUCCESS")

                # Verbalized sampling: counter answer-distribution collapse (arXiv:2607.18310)
                if verbalized_sampling and mode != "Longitudinal Study":
                    vs_note = ("Before answering, briefly consider how people with backgrounds like yours "
                               "might differ in their answers, then give YOUR own answer as one individual.")
                    survey_context = f"{survey_context}\n\n{vs_note}" if survey_context else vs_note
                    add_log("Verbalized sampling enabled", "INFO")

                # Progress callback with logging
                def update_progress(message):
                    status_text.text(message)
                    # Add to log if it's an important message
                    if any(keyword in message for keyword in ["Querying", "Progress", "complete", "Presenting", "Asking"]):
                        if "Querying" in message or "Presenting" in message or "Asking" in message:
                            add_log(message, "REQUEST")
                        elif "Progress" in message:
                            add_log(message, "INFO")
                        elif "complete" in message:
                            add_log(message, "SUCCESS")

                try:
                    # Run simulation based on mode and parallel settings
                    api_provider = st.session_state.get('api_provider', 'Local (LM Studio)')
                    use_parallel = st.session_state.get('enable_parallel', False) and api_provider != "Local (LM Studio)"

                    # Debug info
                    if use_parallel:
                        st.caption(f"Debug: Using parallel mode with {st.session_state.get('parallel_workers', 5)} workers")
                    else:
                        st.caption(f"Debug: Using sequential mode (API: {api_provider})")

                    if mode == "Survey":
                        if use_parallel:
                            # Use parallel async execution for cloud APIs
                            import asyncio

                            from src import ParallelSimulationEngine

                            add_log("Initializing parallel simulation engine", "INFO")
                            status_text.text("Initializing parallel engine...")

                            parallel_engine = ParallelSimulationEngine(
                                llm_client=st.session_state.llm_client,
                                max_workers=st.session_state.get('parallel_workers', 5)
                            )

                            workers = st.session_state.get('parallel_workers', 5)
                            total_requests = len(selected_personas) * len(questions)
                            add_log(f"Parallel mode: {workers} workers, {total_requests} total requests", "INFO")
                            status_text.text("Starting parallel execution...")

                            # Function to check stop flag
                            def check_stop():
                                return st.session_state.get('stop_simulation', False)

                            try:
                                with st.spinner(f"Running {len(selected_personas) * len(questions)} requests in parallel with {st.session_state.get('parallel_workers', 5)} workers..."):
                                    # Get selected model
                                    model = st.session_state.get('selected_model', None)

                                    add_log(f"Using model: {model}", "INFO")
                                    status_text.text(f"Model: {model}, Personas: {len(selected_personas)}, Questions: {len(questions)}")

                                    # Create progress callback that checks stop flag
                                    def progress_with_stop_check(msg):
                                        if check_stop():
                                            parallel_engine.should_stop = True
                                            add_log("Stop signal received", "WARNING")
                                        update_progress(msg)

                                    # Prepare per-question validation if available
                                    per_question_val = None
                                    if response_validations:
                                        # Convert list to dict: {question_index: validation_dict}
                                        per_question_val = {i: v for i, v in enumerate(response_validations) if v is not None}

                                    # Run async simulation
                                    result = asyncio.run(parallel_engine.run_survey_parallel(
                                        personas=selected_personas,
                                        questions=questions,
                                        temperature=temperature,
                                        max_tokens=max_tokens,
                                        progress_callback=progress_with_stop_check,
                                        survey_context=survey_context if survey_context else None,
                                        model=model,
                                        response_validation=response_validation,
                                        per_question_validation=per_question_val,
                                        seed=seed
                                    ))

                                if check_stop():
                                    add_log("Simulation stopped by user", "WARNING")
                                    st.caption("Simulation stopped by user")
                                    st.session_state.simulation_running = False
                                else:
                                    add_log(f"Parallel simulation complete! Collected {len(result.persona_responses)} responses", "SUCCESS")
                                    status_text.text(f"Parallel simulation complete! Got {len(result.persona_responses)} responses")
                            except asyncio.CancelledError:
                                add_log("Simulation cancelled by user", "WARNING")
                                st.caption("Simulation cancelled by user")
                                st.session_state.simulation_running = False
                                st.stop()
                        else:
                            # Sequential execution
                            add_log("Starting sequential survey execution", "INFO")
                            def check_stop():
                                return st.session_state.get('stop_simulation', False)

                            try:
                                with st.spinner("Running survey simulation..."):
                                    # Prepare per-question validation if available
                                    per_question_val = None
                                    if response_validations:
                                        # Convert list to dict: {question_index: validation_dict}
                                        per_question_val = {i: v for i, v in enumerate(response_validations) if v is not None}

                                    result = engine.run_survey(
                                        personas=selected_personas,
                                        questions=questions,
                                        temperature=temperature,
                                        max_tokens=max_tokens,
                                        progress_callback=update_progress,
                                        survey_context=survey_context if survey_context else None,
                                        response_validation=response_validation,
                                        per_question_validation=per_question_val,
                                        survey_config=st.session_state.current_survey_config,
                                        stop_callback=check_stop,
                                        model=st.session_state.get('selected_model'),
                                        seed=seed
                                    )

                                if check_stop():
                                    add_log("Simulation stopped by user", "WARNING")
                                    st.caption("Simulation stopped by user")
                                    st.session_state.simulation_running = False
                                else:
                                    _failed = sum(1 for r in result.persona_responses if str(r.get('response', '')).startswith('[Error:'))
                                    add_log("Sequential survey simulation complete" + (f" — {_failed} request(s) failed, see [Error:] rows" if _failed else ""), "SUCCESS" if not _failed else "WARNING")
                            except Exception as e:
                                add_log(f"Error: {str(e)}", "ERROR")
                                st.error(f"Error during simulation: {str(e)}")
                                st.session_state.simulation_running = False
                                raise

                    elif mode == "Message Testing":
                        add_log("Starting Message Testing mode", "INFO")
                        def check_stop():
                            return st.session_state.get('stop_simulation', False)

                        if use_parallel:
                            # Parallel message testing
                            import asyncio

                            from src import ParallelSimulationEngine

                            add_log("Parallel message testing enabled", "INFO")
                            parallel_engine = ParallelSimulationEngine(
                                llm_client=st.session_state.llm_client,
                                max_workers=st.session_state.get('parallel_workers', 5)
                            )

                            try:
                                def progress_with_stop_check(msg):
                                    if check_stop():
                                        parallel_engine.should_stop = True
                                        add_log("Stop signal received", "WARNING")
                                    update_progress(msg)

                                add_log(f"Showing intervention to {len(selected_personas)} personas", "INFO")
                                with st.spinner(f"Running parallel message testing with {st.session_state.get('parallel_workers', 5)} workers..."):
                                    model = st.session_state.get('selected_model', None)

                                    result = asyncio.run(parallel_engine.run_intervention_parallel(
                                        personas=selected_personas,
                                        intervention_text=intervention_text,
                                        questions=questions,
                                        temperature=temperature,
                                        max_tokens=max_tokens,
                                        progress_callback=progress_with_stop_check,
                                        model=model,
                                        seed=seed,
                                        survey_context=survey_context or None,
                                    ))

                                result.simulation_type = 'message_testing'

                                if check_stop():
                                    add_log("Simulation stopped by user", "WARNING")
                                    st.caption("Simulation stopped by user")
                                    st.session_state.simulation_running = False
                                else:
                                    add_log("Parallel message testing complete", "SUCCESS")
                                    status_text.text("Parallel message testing complete!")
                            except asyncio.CancelledError:
                                add_log("Simulation cancelled by user", "WARNING")
                                st.caption("Simulation cancelled by user")
                                st.session_state.simulation_running = False
                                st.stop()
                        else:
                            # Sequential message testing
                            add_log("Sequential message testing mode", "INFO")
                            try:
                                with st.spinner("Running message testing simulation..."):
                                    result = engine.run_intervention(
                                        personas=selected_personas,
                                        intervention_text=intervention_text,
                                        followup_questions=questions,
                                        temperature=temperature,
                                        max_tokens=max_tokens,
                                        progress_callback=update_progress,
                                        stop_callback=check_stop,
                                        seed=seed,
                                        model=st.session_state.get('selected_model'),
                                        survey_context=survey_context or None,
                                    )
                                    result.simulation_type = 'message_testing'

                                if check_stop():
                                    add_log("Simulation stopped by user", "WARNING")
                                    st.caption("Simulation stopped by user")
                                    st.session_state.simulation_running = False
                                else:
                                    add_log("Message testing complete", "SUCCESS")
                            except Exception as e:
                                add_log(f"Error: {str(e)}", "ERROR")
                                st.error(f"Error during simulation: {str(e)}")
                                st.session_state.simulation_running = False
                                raise

                    elif mode == "A/B Testing":
                        add_log("Starting A/B Testing mode", "INFO")
                        def check_stop():
                            return st.session_state.get('stop_simulation', False)

                        if use_parallel:
                            # Parallel A/B testing
                            import asyncio

                            from src import ParallelSimulationEngine

                            add_log("Parallel A/B testing enabled", "INFO")
                            parallel_engine = ParallelSimulationEngine(
                                llm_client=st.session_state.llm_client,
                                max_workers=st.session_state.get('parallel_workers', 5)
                            )

                            try:
                                def progress_with_stop_check(msg):
                                    if check_stop():
                                        parallel_engine.should_stop = True
                                        add_log("Stop signal received", "WARNING")
                                    update_progress(msg)

                                with st.spinner(f"Running parallel A/B test with {st.session_state.get('parallel_workers', 5)} workers..."):
                                    model = st.session_state.get('selected_model', None)

                                    # Deterministic assignment (same seed as preview) so groups match
                                    assignment_seed = seed if seed is not None else 42
                                    ab_manager = ABTestManager(seed=assignment_seed)
                                    assignments = ab_manager.assign_personas(
                                        personas=selected_personas,
                                        conditions=conditions,
                                        stratify_by=stratify_by.lower().replace(" ", "_") if stratify_by != "None" else None,
                                        random_assignment=random_assignment,
                                    )

                                    def _run_group(personas, questions, survey_context, **kw):
                                        return asyncio.run(parallel_engine.run_survey_parallel(
                                            personas=personas,
                                            questions=questions,
                                            temperature=temperature,
                                            max_tokens=max_tokens,
                                            progress_callback=progress_with_stop_check,
                                            survey_context=survey_context,
                                            model=model,
                                            per_question_validation=st.session_state.get('ab_question_validations') or None,
                                            seed=seed
                                        ))

                                    result = run_ab_test(
                                        _run_group,
                                        personas=selected_personas,
                                        conditions=conditions,
                                        assignments=assignments,
                                        questions=questions,
                                        base_context=survey_context or None,
                                    )

                                if check_stop():
                                    add_log("A/B test stopped by user", "WARNING")
                                    st.caption("A/B test stopped by user")
                                    st.session_state.simulation_running = False
                                else:
                                    add_log("Parallel A/B testing complete", "SUCCESS")
                                    status_text.text("Parallel A/B testing complete!")
                            except asyncio.CancelledError:
                                add_log("A/B test cancelled by user", "WARNING")
                                st.caption("A/B test cancelled by user")
                                st.session_state.simulation_running = False
                                st.stop()
                        else:
                            # Sequential A/B testing: run each condition group with its own context
                            add_log("Sequential A/B testing mode", "INFO")
                            with st.spinner("Running A/B test simulation..."):
                                assignment_seed = seed if seed is not None else 42
                                ab_manager = ABTestManager(seed=assignment_seed)
                                assignments = ab_manager.assign_personas(
                                    personas=selected_personas,
                                    conditions=conditions,
                                    stratify_by=stratify_by.lower().replace(" ", "_") if stratify_by != "None" else None,
                                    random_assignment=random_assignment,
                                )
                                result = run_ab_test(
                                    engine.run_survey,
                                    personas=selected_personas,
                                    conditions=conditions,
                                    assignments=assignments,
                                    questions=questions,
                                    temperature=temperature,
                                    max_tokens=max_tokens,
                                    progress_callback=update_progress,
                                    per_question_validation=st.session_state.get('ab_question_validations') or None,
                                    model=st.session_state.get('selected_model'),
                                    seed=seed,
                                    base_context=survey_context or None,
                                    stop_callback=check_stop,
                                )

                            if check_stop():
                                add_log("A/B test stopped by user", "WARNING")
                                st.caption("A/B test stopped by user")
                                st.session_state.simulation_running = False
                            else:
                                add_log("Sequential A/B testing complete", "SUCCESS")

                    elif mode == "Longitudinal Study":
                        # ============================================================
                        # LONGITUDINAL STUDY EXECUTION
                        # ============================================================
                        add_log("Initializing longitudinal study engine", "INFO")

                        # Create LongitudinalStudyEngine
                        long_engine = LongitudinalStudyEngine(llm_client=st.session_state.llm_client)

                        # Build wave configurations
                        wave_configs = []
                        for idx, wave in enumerate(waves_config):
                            # Determine if this is an intervention wave
                            is_intervention = False
                            wave_intervention_text = None

                            if intervention_text and intervention_wave and idx == intervention_wave:
                                is_intervention = True
                                wave_intervention_text = intervention_text

                            wave_config = WaveConfig(
                                wave_number=idx + 1,
                                wave_name=wave['name'],
                                days_from_baseline=idx * 7,  # Simple 7-day intervals
                                questions=wave['questions'],
                                intervention_text=wave_intervention_text,
                                is_intervention_wave=is_intervention,
                                wave_context=wave['time_description']
                            )
                            wave_configs.append(wave_config)

                        add_log(f"Created {len(wave_configs)} wave configurations", "INFO")

                        # Create study configuration
                        study_config = LongitudinalStudyConfig(
                            study_id=f"study_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                            study_name=study_name,
                            description=f"Longitudinal study with {len(wave_configs)} waves",
                            waves=wave_configs
                        )

                        add_log(f"Study: {study_name}", "INFO")
                        add_log(f"Waves: {len(wave_configs)}", "INFO")
                        if intervention_text and intervention_wave is not None:
                            add_log(f"Intervention at wave {intervention_wave + 1}", "INFO")

                        # Run longitudinal study
                        add_log("Starting longitudinal study execution", "INFO")
                        status_text.text("Running longitudinal study...")

                        def longitudinal_progress(message):
                            status_text.text(message)
                            add_log(message, "INFO")

                        try:
                            with st.spinner("Running longitudinal study across multiple waves..."):
                                longitudinal_result = long_engine.run_study(
                                    personas=selected_personas,
                                    config=study_config,
                                    temperature=temperature,
                                    max_tokens=max_tokens,
                                    seed=seed,
                                    progress_callback=longitudinal_progress
                                )

                            # Count total waves across all personas
                            total_waves = sum(len(wave_results) for wave_results in longitudinal_result.persona_results.values())
                            add_log(f"Longitudinal study complete! {total_waves} persona-waves executed", "SUCCESS")

                            # Convert to standard SimulationResult format for storage
                            # Flatten all persona/wave responses
                            all_responses = []
                            personas_by_id = {p.persona_id: p for p in selected_personas}
                            for persona_id, wave_results in longitudinal_result.persona_results.items():
                                persona = personas_by_id.get(persona_id)
                                for wave_result in wave_results:
                                    for response_item in wave_result.responses:
                                        all_responses.append({
                                            **(SimulationResult.persona_fields(persona) if persona else {
                                                'persona_id': persona_id,
                                                'persona_name': wave_result.persona_name,
                                            }),
                                            'question': f"[{wave_result.wave_name}] {response_item['question']}",
                                            'response': response_item['response'],
                                            'wave': wave_result.wave_name,
                                            'wave_number': wave_result.wave_number,
                                            'timestamp': response_item.get('timestamp', '')
                                        })

                            # Create SimulationResult object
                            from datetime import datetime

                            result = SimulationResult(
                                timestamp=datetime.now().isoformat(),
                                simulation_type='longitudinal_study'
                            )

                            # Set result properties
                            result.persona_responses = all_responses
                            result.questions = [f"[{w.wave_name}] " + ", ".join(w.questions[:2]) + ("..." if len(w.questions) > 2 else "") for w in wave_configs]
                            result.intervention_text = intervention_text if intervention_text else None
                            result.survey_config = {
                                'study_name': study_name,
                                'study_id': study_config.study_id,
                                'n_waves': len(wave_configs),
                                'wave_names': [w.wave_name for w in wave_configs],
                                'has_intervention': intervention_text is not None,
                                'intervention_wave': intervention_wave + 1 if intervention_text and intervention_wave is not None else None,
                                'total_responses': len(all_responses),
                                'longitudinal_summary': {
                                    'total_persona_waves': total_waves,
                                    'personas_count': len(selected_personas),
                                    'waves_config': [w.to_dict() for w in wave_configs]
                                }
                            }
                            result.instrument_name = f"Longitudinal Study: {study_name}"
                            result.metadata.update(longitudinal_result.metadata)

                            add_log(f"Created result with {len(all_responses)} total responses", "SUCCESS")

                        except Exception as e:
                            add_log(f"Longitudinal study error: {str(e)}", "ERROR")
                            import traceback
                            add_log(f"Traceback: {traceback.format_exc()[:500]}", "ERROR")
                            raise e

                    progress_bar.progress(100)
                    add_log("Simulation complete!", "SUCCESS")
                    status_text.text("Simulation complete!")

                    # Show performance stats if available
                    if cache:
                        stats = engine.get_performance_stats()

                        add_log("Generating performance statistics", "INFO")

                        perf_col1, perf_col2 = st.columns(2)

                        with perf_col1:
                            if stats['response_times']['count'] > 0:
                                avg_time = stats['response_times']['mean']
                                st.metric("Avg Response Time", f"{avg_time:.2f}s")
                                add_log(f"Average response time: {avg_time:.2f}s", "INFO")

                        with perf_col2:
                            if 'cache' in stats:
                                hit_rate = stats['cache']['hit_rate']
                                hits = stats['cache']['hits']
                                st.metric("Cache Hit Rate", f"{hit_rate:.1%}",
                                         help=f"Saved {hits} LLM calls")
                                add_log(f"Cache hits: {hits} ({hit_rate:.1%})", "CACHE")

                    # Save results
                    result.metadata.update({
                        'population_size': len(selected_personas),
                        'persona_ids': [p.persona_id for p in selected_personas],
                        'temperature': temperature,
                        'max_tokens': int(max_tokens),
                        'provider': api_provider,
                        'verbalized_sampling': bool(verbalized_sampling),
                    })
                    add_log("Saving results to storage", "INFO")
                    csv_file, json_file = st.session_state.results_storage.save_results(result)
                    add_log(f"Results saved: {csv_file}", "SUCCESS")
                    add_log(f"Results saved: {json_file}", "SUCCESS")

                    st.caption(f"Simulation complete! Results saved to `{csv_file}` and `{json_file}`")

                    # Display preview
                    with results_container:
                        st.markdown("**Results Preview**")

                        # Show summary
                        st.write(f"**Personas:** {len(selected_personas)}")
                        st.write(f"**Questions:** {len(questions)}")
                        st.write(f"**Total Responses:** {len(result.persona_responses)}")
                        invalid_count = sum(
                            r.get('validation_status') == 'invalid' or
                            str(r.get('response', '')).startswith('[Error:')
                            for r in result.persona_responses
                        )
                        if invalid_count:
                            st.warning(f"{invalid_count} response(s) failed generation or validation and were preserved for audit, not silently rewritten.")

                        add_log(f"Generated {len(result.persona_responses)} total responses", "SUCCESS")

                        # Show sample responses
                        with st.expander("View Sample Responses", expanded=True):
                            for i, response_data in enumerate(result.persona_responses[:5]):  # Show first 5
                                st.markdown(f"**{response_data['persona_name']}** - *{response_data['question']}*")
                                st.write(response_data['response'])
                                st.markdown("---")

                            if len(result.persona_responses) > 5:
                                st.caption(f"... and {len(result.persona_responses) - 5} more responses. View all in the Results page.")

                        # Navigation button
                        if st.button("View Full Results", type="primary"):
                            st.switch_page("pages/3_Results.py")

                except Exception as e:
                    add_log(f"EXCEPTION: {str(e)}", "ERROR")
                    add_log(f"Exception type: {type(e).__name__}", "ERROR")
                    st.error(f"Error during simulation: {str(e)}")
                    st.error(f"Error type: {type(e).__name__}")
                    # Show full traceback for debugging
                    import traceback
                    tb = traceback.format_exc()
                    add_log(f"Traceback: {tb[:200]}...", "ERROR")  # Log first 200 chars of traceback
                    st.code(tb)
                    progress_bar.empty()
                    status_text.empty()

                finally:
                    add_log("Cleaning up simulation state", "INFO")
                    st.session_state.simulation_running = False
                    add_log(f"Total log entries: {len(st.session_state.simulation_logs)}", "INFO")

        else:
            st.caption("To run: " + " · ".join(missing))
            if not llm_ready and st.button("Go to Setup to connect a model →"):
                st.switch_page("pages/1_Setup.py")

# ---- Wizard nav ----
st.markdown("---")
_can_next = (step == 1 or (step == 2 and len(selected_personas) > 0)
             or (step == 3 and not _config_blockers))
nav_l, _nav_m, nav_r = st.columns([1, 5, 1])
with nav_l:
    if st.button("← Back", disabled=(step == 1), use_container_width=True):
        st.session_state.sim_step = max(1, step - 1)
        st.rerun()
with nav_r:
    if step < 4 and st.button("Next →", type="primary",
                              disabled=not _can_next, use_container_width=True):
        st.session_state.sim_step = step + 1
        st.rerun()
if step == 3 and not _can_next:
    st.caption("Finish this step first: " + " · ".join(_config_blockers))
