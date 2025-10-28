"""Simulation page for running surveys and interventions."""
import streamlit as st
import json
from datetime import datetime
from src import (
    PersonaManager, LMStudioClient, SimulationEngine, ResultsStorage,
    SurveyTemplateLibrary, SurveyConfig, SurveyConfigManager,
    QuestionMetadata, SurveySection, render_navigation,
    ABTestManager, Condition, ABTestConfig, render_system_status_badge,
    LongitudinalStudyEngine, WaveConfig, LongitudinalStudyConfig,
    LongitudinalStudyBuilder
)
from src.styles import apply_global_styles

st.set_page_config(page_title="Simulation - LLM Simulation", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

# Apply global design system
apply_global_styles()

# Top Navigation
render_navigation(current_page="simulation")

# System Status Sidebar
render_system_status_badge()

# Hero Section
st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    color: white;
">
    <h1 style="color: white; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">
        🎯 Survey & Message Testing
    </h1>
    <p style="color: rgba(255,255,255,0.95); font-size: 1.1rem; line-height: 1.6; margin-bottom: 0;">
        Run AI-powered simulations to test surveys, messages, and interventions across diverse personas.
    </p>
</div>
""", unsafe_allow_html=True)

# Add clarification about different simulation types
st.markdown("""
<div style="
    background: white;
    border-left: 4px solid #667eea;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
">
    <p style="margin: 0; line-height: 1.8;">
        <strong>📋 Survey Mode:</strong> Ask questions directly to get opinions and responses<br>
        <strong>💬 Message Testing Mode:</strong> Test how personas react to messages/interventions
    </p>
</div>
""", unsafe_allow_html=True)

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

# Initialize variables for all modes
questions = []
intervention_text = ""
conditions = []
survey_context = ""
response_validation = None

# Check connection
if not st.session_state.llm_client:
    st.error("⚠️ Not connected to LM Studio. Please go to the Setup page and test your connection.")
    st.stop()

# Load personas: disk personas (permanent) + session personas (temporary from CSV uploads) + generated personas
disk_personas = st.session_state.persona_manager.load_all_personas()
session_personas = st.session_state.session_personas if 'session_personas' in st.session_state else []
generated_personas = st.session_state.generated_personas if 'generated_personas' in st.session_state else []
personas = disk_personas + session_personas + generated_personas

if not personas:
    st.warning("No personas available. Please create personas in the Setup page first.")
    st.stop()

# Simulation mode selection
st.subheader("1. Select Simulation Mode")

# Add clear descriptions for each mode
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📋 Survey Mode**
    - Ask questions directly to synthetic personas
    - Get immediate responses and opinions
    - Perfect for: Market research, opinion polls, needs assessment
    """)

with col2:
    st.markdown("""
    **💬 Message Testing Mode**
    - Present information/messages to personas first
    - Then ask follow-up questions about their reactions
    - Perfect for: Testing messaging, intervention attitudes, communication strategies
    """)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    **🧪 A/B Testing Mode**
    - Compare multiple intervention conditions
    - Random assignment of personas to conditions
    - Perfect for: Experimental design, intervention comparison
    """)

with col4:
    st.markdown("""
    **📊 Analysis Features**
    - Compare responses across conditions
    - View response patterns
    - Perfect for: Understanding differences between groups
    """)

# Add Longitudinal Study description
st.markdown("""
**📈 Longitudinal Study Mode**
- Track changes across multiple time points (waves)
- Personas remember previous responses
- Test intervention effects over time
- Perfect for: Pre-post studies, behavior change tracking
""")

mode = st.radio(
    "Choose simulation type:",
    ["Survey", "Message Testing", "A/B Testing", "Longitudinal Study"],
    horizontal=True,
    help="Survey: Direct questions. Message Testing: Present info first. A/B Testing: Compare conditions. Longitudinal: Multi-wave tracking."
)

st.markdown("---")

# Persona selection
st.subheader("2. Select Personas")

col1, col2 = st.columns([1, 3])

with col1:
    select_all = st.checkbox("Select All", value=True)

with col2:
    if select_all:
        selected_personas = st.multiselect(
            "Choose personas to include:",
            personas,
            default=personas,
            format_func=lambda p: f"{p.name} ({p.age}, {p.occupation}) {'[Generated]' if p in generated_personas else '[Permanent]' if p in disk_personas else '[Temporary]'}",
            key="persona_select"
        )
    else:
        selected_personas = st.multiselect(
            "Choose personas to include:",
            personas,
            format_func=lambda p: f"{p.name} ({p.age}, {p.occupation}) {'[Generated]' if p in generated_personas else '[Permanent]' if p in disk_personas else '[Temporary]'}",
            key="persona_select"
        )

if not selected_personas:
    st.info("👆 Please select at least one persona to continue.")
    st.stop()

st.success(f"Selected {len(selected_personas)} persona(s)")

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

st.markdown("---")

# ============================================================================
# SECTION 3: COMPREHENSIVE SURVEY CONFIGURATION
# ============================================================================
st.subheader("3. Configure Simulation")

# Research Design Information Cards
st.markdown("""
<div style="margin: 1.5rem 0;">
    <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 1rem;">
        💡 <strong>Supported Research Designs</strong> - Choose the best method for your research question
    </p>
</div>
""", unsafe_allow_html=True)

# Create info cards for different research designs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        height: 100%;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    ">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📋</div>
        <div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">Cross-Sectional Survey</div>
        <div style="font-size: 0.85rem; line-height: 1.5; opacity: 0.95;">
            Single measurement, quick opinion collection.<br/>
            <strong>Best for:</strong> Market research, needs assessment, status quo
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        height: 100%;
        box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);
    ">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">💬</div>
        <div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">Message Testing</div>
        <div style="font-size: 0.85rem; line-height: 1.5; opacity: 0.95;">
            Test message impact on different groups.<br/>
            <strong>Best for:</strong> Health communication, ad effectiveness, persuasion
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        height: 100%;
        box-shadow: 0 4px 12px rgba(79, 172, 254, 0.3);
    ">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧪</div>
        <div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">A/B Testing</div>
        <div style="font-size: 0.85rem; line-height: 1.5; opacity: 0.95;">
            Randomized control, compare conditions.<br/>
            <strong>Best for:</strong> Intervention comparison, optimization, causal inference
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        height: 100%;
        box-shadow: 0 4px 12px rgba(67, 233, 123, 0.3);
    ">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📈</div>
        <div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">Longitudinal Study</div>
        <div style="font-size: 0.85rem; line-height: 1.5; opacity: 0.95;">
            Multi-wave tracking, observe trends.<br/>
            <strong>Best for:</strong> Behavior change, intervention effects, trajectories
        </div>
    </div>
    """, unsafe_allow_html=True)

# Design comparison table (collapsible)
with st.expander("📊 Detailed Comparison - Choose the Right Design"):
    st.markdown("""
    | Design Type | Measurements | Causal Inference | Time Cost | Best Use Cases | Key Advantages |
    |-------------|--------------|------------------|-----------|----------------|----------------|
    | **📋 Cross-Sectional** | 1 time | ❌ None | ⚡ Low | Quick insights, exploratory research | Fast, low-cost, easy to implement |
    | **💬 Message Testing** | 1 + intervention | ⚠️ Weak | ⚡ Low | Test messaging, information acceptance | Realistic reactions, immediate feedback |
    | **🧪 A/B Testing** | 1 + control | ✅ Strong | ⚡⚡ Medium | Compare options, optimize decisions | Random assignment, high internal validity |
    | **📈 Longitudinal** | Multiple waves | ✅ Strong | ⚡⚡⚡ High | Track changes, long-term effects | Observe trends, conversation memory |
    
    ---
    
    ### 🎯 Design Selection Guide
    
    **When to choose Cross-Sectional Survey?**
    - ✅ Need quick understanding of population opinions and attitudes
    - ✅ Exploratory research to identify research questions
    - ✅ Limited resources, need efficient data collection
    - ❌ Not suitable for: Studies requiring causal proof
    
    **When to choose Message Testing?**
    - ✅ Evaluate health messages or ad copy effectiveness
    - ✅ Test different framing approaches
    - ✅ Understand how information changes attitudes
    - ❌ Not suitable for: Long-term tracking studies
    
    **When to choose A/B Testing?**
    - ✅ Need to compare 2-5 different approaches
    - ✅ Require high internal validity (clear causation)
    - ✅ Have sufficient sample size for groups
    - ❌ Not suitable for: Single intervention condition studies
    
    **When to choose Longitudinal Study?**
    - ✅ Evaluate long-term intervention effects
    - ✅ Track behavior change trajectories
    - ✅ Study development and change processes
    - ✅ Need personas to "remember" previous interactions
    - ❌ Not suitable for: Time-sensitive rapid research
    
    ---
    
    ### 💡 Combined Design Recommendations
    
    Many studies can combine multiple designs:
    
    - **Longitudinal + A/B**: Compare long-term effects of multiple interventions (e.g., compare 3 smoking cessation methods over 6 months)
    - **Message Testing + Cross-Sectional**: Test message effectiveness first, then conduct large-scale attitude survey
    - **A/B + Longitudinal**: Random assignment followed by multiple follow-ups (classic RCT design)
    """)

st.markdown("---")

if mode == "Survey":
    # Create tabs for different configuration methods
    config_tab1, config_tab2 = st.tabs([
        "📋 Quick Start (Templates)",
        "🤖 AI-Powered Survey Parser"
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
            
            st.info(f"**Description:** {template.description}")
            
            # Preview questions
            with st.expander("🔍 Preview Questions"):
                questions_list = template.get_all_questions()
                for i, q in enumerate(questions_list, 1):
                    reverse_marker = " 🔄" if q.reverse_scored else ""
                    st.write(f"{i}. {q.text}{reverse_marker}")
                    if q.scale_labels:
                        labels_str = ', '.join([f'{k}={v}' for k, v in sorted(q.scale_labels.items())])
                        st.caption(f"   Scale: {q.scale_min}-{q.scale_max}: {labels_str}")
            
            # Response Format Enforcement for Templates
            st.markdown("---")
            st.markdown("#### 🔒 Response Format (Optional)")
            
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
                    st.success(f"✅ Responses will be enforced as numbers between {min_val}-{max_val}")
                
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
                        st.success(f"✅ Responses must be one of: {', '.join(words_list)}")
                
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
                    st.success("✅ Responses will be enforced as JSON objects")
            else:
                st.session_state.template_response_validation = None
            
            # Load button
            st.markdown("---")
            if st.button("✅ Load This Template", type="primary", use_container_width=True):
                # Create config from template
                st.session_state.current_survey_config = SurveyConfig.from_template(template)
                st.success(f"✅ Loaded {selected_template}! You can customize it or run the simulation directly.")
                st.rerun()
    
    # ========================================================================
    # TAB 2: AI-POWERED SURVEY PARSER
    # ========================================================================
    with config_tab2:
        st.markdown("### 🤖 AI-Powered Survey Parser")
        st.write("Paste your survey text in natural language, and let AI extract the structure automatically!")
        
        # Survey Metadata
        st.markdown("#### 📝 Survey Metadata")
        col1, col2 = st.columns(2)
        
        with col1:
            survey_title = st.text_input(
                "Survey Title *",
                value=st.session_state.current_survey_config.title if st.session_state.current_survey_config else "",
                placeholder="e.g., Mental Health Survey 2024"
            )
        
        with col2:
            time_reference = st.text_input(
                "Time Reference",
                value=st.session_state.current_survey_config.time_reference if st.session_state.current_survey_config else "",
                placeholder="e.g., Over the last 2 weeks, Currently, In the past month"
            )
        
        survey_description = st.text_area(
            "Description",
            value=st.session_state.current_survey_config.description if st.session_state.current_survey_config else "",
            placeholder="Brief description of the survey purpose",
            height=60
        )
        
        survey_purpose = st.text_area(
            "Purpose/Goal",
            value=st.session_state.current_survey_config.purpose if st.session_state.current_survey_config else "",
            placeholder="What research question does this survey address?",
            height=60
        )
        
        st.markdown("---")
        
        # Instructions
        st.markdown("#### 📋 Survey Instructions")
        
        pre_survey_text = st.text_area(
            "Pre-Survey Context (optional)",
            value=st.session_state.current_survey_config.pre_survey_text if st.session_state.current_survey_config else "",
            placeholder="Scenario or context to present before the survey (e.g., 'Imagine you are considering a new health policy...')",
            height=80
        )
        
        instructions = st.text_area(
            "General Instructions *",
            value=st.session_state.current_survey_config.instructions if st.session_state.current_survey_config else "",
            placeholder="I am a PI of a health survey. Thank you for participating. Please respond using: 0 = Rarely/none of the time; 1 = Some or a little of the time; 2 = Occasionally/moderate amount; 3 = Most/all of the time",
            height=100
        )
        
        st.markdown("---")
        
        # Questions Input Method
        st.markdown("#### ❓ Questions Configuration")
        
        input_method = st.radio(
            "Input Method:",
            ["Bulk Text Entry", "Individual Question Editor"],
            horizontal=True
        )
        
        if input_method == "Bulk Text Entry":
            questions_text = st.text_area(
                "Questions (one per line) *",
                placeholder="I felt sad or depressed.\nI had trouble sleeping.\nI felt hopeful about the future.",
                height=200,
                help="Enter each question on a new line"
            )
            
            # Parse questions
            if questions_text:
                question_texts = [q.strip() for q in questions_text.split('\n') if q.strip()]
                st.info(f"📝 {len(question_texts)} question(s) entered")
            else:
                question_texts = []
        
        else:  # Individual Question Editor
            st.write("Add questions one at a time with detailed metadata:")
            
            if 'custom_questions' not in st.session_state:
                st.session_state.custom_questions = []
            
            with st.form("add_question_form"):
                q_text = st.text_input("Question Text *")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    q_scale_min = st.number_input("Scale Min", value=0, step=1)
                with col_b:
                    q_scale_max = st.number_input("Scale Max", value=3, step=1)
                with col_c:
                    q_reverse = st.checkbox("Reverse Scored")
                
                q_instrument = st.text_input("Instrument/Source", placeholder="e.g., PHQ-9, Custom")
                q_notes = st.text_input("Notes", placeholder="e.g., Item 1, Depression subscale")
                
                if st.form_submit_button("➕ Add Question"):
                    if q_text:
                        st.session_state.custom_questions.append({
                            'text': q_text,
                            'scale_min': q_scale_min,
                            'scale_max': q_scale_max,
                            'reverse_scored': q_reverse,
                            'instrument': q_instrument,
                            'notes': q_notes
                        })
                        st.success(f"Added question {len(st.session_state.custom_questions)}")
                        st.rerun()
            
            # Show added questions
            if st.session_state.custom_questions:
                st.write(f"**Added Questions ({len(st.session_state.custom_questions)}):**")
                for i, q in enumerate(st.session_state.custom_questions):
                    with st.expander(f"Q{i+1}: {q['text'][:50]}..."):
                        st.write(f"**Text:** {q['text']}")
                        st.write(f"**Scale:** {q['scale_min']}-{q['scale_max']}")
                        if q['reverse_scored']:
                            st.write("**🔄 Reverse Scored**")
                        if q['instrument']:
                            st.write(f"**Instrument:** {q['instrument']}")
                        if q['notes']:
                            st.write(f"**Notes:** {q['notes']}")
                        
                        if st.button(f"🗑️ Remove Q{i+1}", key=f"remove_{i}"):
                            st.session_state.custom_questions.pop(i)
                            st.rerun()
                
                question_texts = [q['text'] for q in st.session_state.custom_questions]
            else:
                st.info("No questions added yet. Use the form above to add questions.")
                question_texts = []
        
        st.markdown("---")
        
        # Response Format Enforcement
        st.markdown("#### 🔒 Response Format")
        
        enforce_format = st.checkbox(
            "Enforce strict response format",
            value=False,
            help="Force responses to follow a specific format"
        )
        
        response_validation = None
        
        if enforce_format:
            format_type = st.selectbox(
                "Format Type:",
                ["Single Number", "Single Word", "JSON Object"],
                help="Choose the response format"
            )
            
            if format_type == "Single Number":
                col_x, col_y = st.columns(2)
                with col_x:
                    min_val = st.number_input("Min Value", value=0, step=1, key="fmt_min")
                with col_y:
                    max_val = st.number_input("Max Value", value=3, step=1, key="fmt_max")
                
                response_validation = {
                    "type": "number",
                    "min": min_val,
                    "max": max_val,
                    "instruction": f"You MUST respond with ONLY a single number between {min_val} and {max_val}. No explanation, just the number."
                }
                st.success(f"✅ Responses will be numbers between {min_val}-{max_val}")
            
            elif format_type == "Single Word":
                allowed_words = st.text_input(
                    "Allowed words (comma-separated):",
                    placeholder="yes, no, maybe"
                )
                if allowed_words:
                    words_list = [w.strip() for w in allowed_words.split(',')]
                    response_validation = {
                        "type": "word",
                        "allowed": words_list,
                        "instruction": f"You MUST respond with ONLY one of these words: {', '.join(words_list)}. No explanation."
                    }
                    st.success(f"✅ Responses must be one of: {', '.join(words_list)}")
    
    # ========================================================================
    # TAB 2: AI-POWERED SURVEY PARSER
    # ========================================================================
    with config_tab2:
        st.markdown("### 🤖 AI-Powered Survey Parser")
        st.info("Paste your survey text below and let AI extract the instructions and questions automatically.")
        
        survey_text = st.text_area(
            "Paste Survey Text Here:",
            placeholder="Example:\n\nI am a PI of a health survey, thanks for your participation. I will ask about your feelings recently. Please respond using:\n0 = Rarely/none of the time\n1 = Some or a little of the time\n2 = Occasionally/moderate amount\n3 = Most/all of the time\n\n1. I felt sad or depressed.\n2. I had trouble sleeping.\n3. I felt hopeful about the future.\n...",
            height=300,
            help="Paste your complete survey text including instructions and questions"
        )
        
        col_parse, col_clear = st.columns([3, 1])
        
        with col_parse:
            parse_button = st.button("🔍 Parse with AI", type="primary", use_container_width=True)
        
        with col_clear:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.parsed_survey = None
                st.rerun()
        
        if parse_button and survey_text:
            with st.spinner("🤖 AI is analyzing your survey text..."):
                try:
                    # Use LLM to parse the survey text
                    parse_prompt = f"""You are a survey analysis expert. Parse the following survey text and extract:
1. Instructions/context (the introductory text explaining the survey)
2. Individual questions (numbered list)

Survey Text:
{survey_text}

Respond in JSON format:
{{
    "instructions": "extracted instructions here",
    "questions": ["question 1", "question 2", ...]
}}

Only return the JSON, no additional text."""

                    response = st.session_state.llm_client.chat_completion(
                        messages=[{"role": "user", "content": parse_prompt}],
                        temperature=0.1,
                        max_tokens=2000
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
                    st.success("✅ Survey parsed successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Failed to parse survey: {str(e)}")
                    st.info("Please ensure you're connected to an LLM (check Home page) and the survey text is clear.")
        
        # Display parsed results if available
        if hasattr(st.session_state, 'parsed_survey') and st.session_state.parsed_survey:
            st.markdown("---")
            st.markdown("### ✅ Parsed Survey")
            
            parsed = st.session_state.parsed_survey
            
            # Editable instructions
            instructions = st.text_area(
                "Instructions (editable):",
                value=parsed.get("instructions", ""),
                height=100
            )
            
            # Editable questions
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
            
            # Add more questions button
            if st.button("➕ Add Another Question"):
                st.session_state.parsed_survey["questions"].append("")
                st.rerun()
            
            # Use these for simulation
            if question_texts:
                st.success(f"✅ Ready to use: {len(question_texts)} questions")
                # Store for simulation below
                st.session_state.ai_parsed_questions = question_texts
                st.session_state.ai_parsed_instructions = instructions
    
    # ========================================================================
    # FINAL SURVEY SETUP (appears below all tabs)
    # ========================================================================
    st.markdown("---")
    st.markdown("### 📊 Current Survey Setup")
    
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
        
        st.success(f"✅ Using: **{config.title}** ({len(questions)} questions)")
    elif hasattr(st.session_state, 'ai_parsed_questions') and st.session_state.ai_parsed_questions:
        # Use AI-parsed questions from tab 2
        questions = st.session_state.ai_parsed_questions
        survey_context = st.session_state.ai_parsed_instructions if hasattr(st.session_state, 'ai_parsed_instructions') else ""
        st.success(f"🤖 Using AI-parsed survey: {len(questions)} questions")
    else:
        st.warning("⚠️ No survey configured. Please use one of the tabs above to configure your survey.")
    
    # Show preview if questions exist
    if questions:
        with st.expander("👀 Preview Complete Survey"):
            if survey_context:
                st.markdown("**Instructions:**")
                st.info(survey_context)
                st.markdown("---")
            
            st.markdown("**Questions:**")
            for i, q in enumerate(questions, 1):
                st.write(f"{i}. {q}")
    
    # Get response validation from template settings if available
    response_validation = None
    if hasattr(st.session_state, 'template_response_validation') and st.session_state.template_response_validation:
        response_validation = st.session_state.template_response_validation
        # Show validation info
        if response_validation:
            st.info(f"🔒 Response Format: {response_validation.get('instruction', 'Custom validation enabled')}")

elif mode == "Message Testing":
    st.write("**Message Testing Mode**: Present information/message, then ask follow-up questions about reactions")
    
    # Create tabs for intervention configuration
    interv_tab1, interv_tab2 = st.tabs([
        "📝 Manual Entry",
        "🤖 AI-Powered Generator"
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
            st.success(f"✅ Message prepared with {len(questions)} follow-up question(s)")
        elif not intervention_text:
            st.warning("Please enter intervention text")
        elif not questions:
            st.warning("Please enter at least one follow-up question")
    
    # ========================================================================
    # INTERVENTION TAB 2: AI-POWERED GENERATOR
    # ========================================================================
    with interv_tab2:
        st.markdown("### 🤖 AI-Powered Message Generator")
        st.info("Describe your intervention scenario in natural language, and AI will generate the intervention text and follow-up questions!")
        
        intervention_description = st.text_area(
            "Describe Your Message/Intervention Scenario:",
            placeholder="Example:\n\nI want to test how people react to a new health policy proposal. The intervention should explain that the government is considering mandatory health screenings for adults over 40. It would be free and take 30 minutes. I want to know if people would support it, what concerns they have, and how it might affect their behavior.",
            height=200,
            help="Describe your intervention in natural language - AI will generate structured content"
        )
        
        col_gen, col_clear = st.columns([3, 1])
        
        with col_gen:
            generate_button = st.button("🔍 Generate Message", type="primary", use_container_width=True)
        
        with col_clear:
            if st.button("🗑️ Clear", key="clear_intervention", use_container_width=True):
                st.session_state.parsed_intervention = None
                st.rerun()
        
        if generate_button and intervention_description:
            with st.spinner("🤖 AI is generating your intervention..."):
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
                    st.success("✅ Message generated successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Failed to generate intervention: {str(e)}")
                    st.info("Please ensure you're connected to an LLM (check Home page) and try again.")
        
        # Display generated results if available
        if hasattr(st.session_state, 'parsed_intervention') and st.session_state.parsed_intervention:
            st.markdown("---")
            st.markdown("### ✅ Generated Message")
            
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
            if st.button("➕ Add Another Question", key="add_interv_question"):
                st.session_state.parsed_intervention["follow_up_questions"].append("")
                st.rerun()
            
            # Use these for simulation (store the edited values)
            if intervention_text and questions:
                st.success(f"✅ Ready to use: Message + {len(questions)} questions")
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
    st.subheader("🧪 A/B Test Configuration")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        test_name = st.text_input(
            "Test Name:",
            value="Intervention Comparison Test",
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
            help="Group personas by demographic characteristics"
        )
        
        random_assignment = st.checkbox(
            "Random Assignment",
            value=True,
            help="Randomly assign personas to conditions"
        )
    
    st.markdown("---")
    
    # Create tabs for condition configuration
    condition_tab1, condition_tab2 = st.tabs([
        "📝 Manual Entry",
        "🤖 AI-Powered Generator"
    ])
    
    # ========================================================================
    # CONDITION TAB 1: MANUAL ENTRY
    # ========================================================================
    with condition_tab1:
        st.subheader("📝 Define Conditions Manually")
        
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
        st.subheader("🤖 AI One-Click Generator")
        st.info("📝 Describe your A/B test in natural language, and AI will generate everything needed!")
        
        # Show examples
        with st.expander("💡 Examples: What to write"):
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
            "🗣️ Describe Your A/B Test:",
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
        if st.button("🚀 Generate Complete A/B Test", type="primary", use_container_width=True):
            if not test_description or len(test_description.strip()) < 20:
                st.warning("⚠️ Please provide a more detailed description (at least 20 characters)")
            else:
                with st.spinner("🤖 AI is generating your complete A/B test setup..."):
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
                                
                                st.success(f"✅ Generated complete A/B test: {ab_test_data.get('test_name', 'Unnamed Test')}")
                                
                                # Display preview
                                st.markdown("---")
                                st.subheader("📋 Generated Test Preview")
                                
                                # Test info
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Test Name", ab_test_data.get('test_name', 'N/A'))
                                    st.metric("Conditions", len(ai_conditions))
                                with col2:
                                    st.metric("Questions", len(ab_test_data['questions']))
                                    st.metric("Target", ab_test_data.get('target_audience', 'General'))
                                
                                # Show conditions
                                st.markdown("**🔀 Test Conditions:**")
                                for i, condition in enumerate(ai_conditions):
                                    with st.expander(f"✅ {condition.condition_name}", expanded=True):
                                        st.write(condition.intervention_text)
                                
                                # Show questions
                                st.markdown("**❓ Follow-up Questions:**")
                                for i, q in enumerate(ab_test_data['questions'], 1):
                                    st.write(f"{i}. {q}")
                                
                                st.success("👉 Scroll down to see assignment preview and start simulation!")
                                
                            else:
                                st.error("❌ AI response missing required fields (conditions or questions)")
                                st.text_area("Raw AI Response:", response, height=200)
                        else:
                            st.error("❌ Could not parse JSON from AI response")
                            st.text_area("Raw AI Response:", response, height=200)
                    
                    except json.JSONDecodeError as e:
                        st.error(f"❌ JSON parsing failed: {str(e)}")
                        st.info("💡 Tip: Try rephrasing your description more clearly")
                        with st.expander("Show raw AI response"):
                            st.text_area("Raw Response:", response, height=200)
                    
                    except Exception as e:
                        st.error(f"❌ Generation failed: {str(e)}")
                        st.info("Make sure you're connected to an LLM (check Home page)")
        
        # Show AI-generated conditions if available
        if 'ai_parsed_conditions' in st.session_state and st.session_state.ai_parsed_conditions:
            st.markdown("---")
            st.subheader("✅ AI-Generated Test Ready")
            st.info("👇 Your AI-generated A/B test is ready. You can modify conditions in the Manual Entry tab if needed.")
            
            # Option to clear and regenerate
            if st.button("🗑️ Clear & Start Over", type="secondary"):
                st.session_state.ai_parsed_conditions = []
                st.session_state.ai_generated_questions = []
                if 'ai_complete_test' in st.session_state:
                    del st.session_state.ai_complete_test
                if 'ai_generated_conditions' in st.session_state:
                    del st.session_state.ai_generated_conditions
                st.rerun()
    
    st.markdown("---")
    
    # Follow-up questions
    st.subheader("❓ Follow-up Questions")
    st.info("These questions will be asked to all participants after they receive their assigned condition.")
    
    # Pre-fill with AI-generated questions if available
    default_questions = ""
    if 'ai_generated_questions' in st.session_state and st.session_state.ai_generated_questions:
        default_questions = "\n".join(st.session_state.ai_generated_questions)
        st.success(f"✅ Using {len(st.session_state.ai_generated_questions)} AI-generated questions (you can edit them below)")
    
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
        st.subheader("📋 Response Format Requirements (Optional)")
        st.caption("Configure specific response formats for each question. Leave blank for open-ended responses.")
        
        # Initialize session state for question validations
        if 'ab_question_validations' not in st.session_state:
            st.session_state.ab_question_validations = {}
        
        question_validations = {}
        
        with st.expander("⚙️ Configure Response Formats", expanded=False):
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
                        st.info("📝 Will encourage 2-4 sentence responses")
                        
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
                    question_validations[i] = {
                        'instruction': instruction,
                        'type': format_type
                    }
                
                st.markdown("---")
        
        # Store in session state
        st.session_state.ab_question_validations = question_validations
        
        if question_validations:
            st.success(f"✅ {len(question_validations)} questions have specific format requirements")
    
    # Use AI-generated conditions if available, otherwise use manual conditions
    if 'ai_parsed_conditions' in st.session_state and st.session_state.ai_parsed_conditions:
        conditions = st.session_state.ai_parsed_conditions
    
    if len(conditions) >= 2 and questions:
        st.success(f"✅ A/B Test configured: {len(conditions)} conditions, {len(questions)} questions")
        
        # Show assignment preview
        if selected_personas:
            st.subheader("👥 Assignment Preview")
            
            # Create test config
            test_config = ABTestConfig(
                test_name=test_name,
                conditions=conditions,
                questions=questions,
                random_assignment=random_assignment,
                stratify_by=stratify_by.lower().replace(" ", "_") if stratify_by != "None" else None
            )
            
            # Assign personas to conditions
            assignments = st.session_state.ab_test_manager.assign_personas(
                personas=selected_personas,
                conditions=conditions,
                stratify_by=test_config.stratify_by
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
            with st.expander("📊 Detailed Assignment"):
                assignment_df = []
                for persona_name, condition_id in assignments.items():
                    # Find the actual Persona object by name
                    persona_obj = next((p for p in selected_personas if p.name == persona_name), None)
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
            st.warning("Please define at least 2 conditions")
        if not questions:
            st.warning("Please enter at least one follow-up question")
    
    # Store for simulation
    intervention_text = ""  # Not used in A/B testing
    survey_context = ""
    response_validation = None

elif mode == "Longitudinal Study":
    st.write("**📈 Longitudinal Study Mode**: Track changes across multiple time points with conversation memory")
    
    st.info("""
    💡 **How it works**: Personas remember all previous interactions. Each wave builds on previous responses, 
    creating realistic behavior change patterns over time.
    """)
    
    # ========================================================================
    # LONGITUDINAL STUDY CONFIGURATION
    # ========================================================================
    st.subheader("📊 Study Design")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        study_name = st.text_input(
            "Study Name:",
            value="Longitudinal Behavior Change Study",
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
            st.info("🔄 Wave 1 (Pre) → 💊 Intervention → Wave 2 (Post)")
        elif study_type == "Repeated Measures (no intervention)":
            st.info("📊 Wave 1 → Wave 2 → Wave 3 (natural progression)")
        else:
            st.info("🔄 Wave 1 (Pre) → 💊 Intervention → Waves 2-N (Multiple follow-ups)")
    
    st.markdown("---")
    
    # ========================================================================
    # WAVE CONFIGURATION
    # ========================================================================
    st.subheader("🔄 Configure Each Wave")
    
    # Initialize waves storage
    if 'longitudinal_waves' not in st.session_state:
        st.session_state.longitudinal_waves = []
    
    waves_config = []
    
    for wave_idx in range(int(n_waves)):
        with st.expander(f"📊 Wave {wave_idx + 1} Configuration", expanded=(wave_idx == 0)):
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
        st.subheader("💊 Intervention Configuration")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            intervention_wave = st.number_input(
                "Apply Intervention After Wave:",
                min_value=1,
                max_value=int(n_waves) - 1,
                value=1,
                help="Intervention will be shown after this wave"
            )
            
            st.info(f"Timeline: Wave {intervention_wave} → 💊 Intervention → Wave {intervention_wave + 1}")
        
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
        st.subheader("📋 Study Summary")
        
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
            if intervention_text:
                total_responses += len(selected_personas)  # Intervention acknowledgment
            st.metric("Total Responses", total_responses)
        
        # Show timeline visualization
        with st.expander("🗓️ Study Timeline"):
            timeline_text = ""
            for i, wave in enumerate(waves_config):
                timeline_text += f"**{wave['name']}** ({wave['time_description']})\n"
                timeline_text += f"  - {len(wave['questions'])} questions\n"
                
                # Add intervention marker
                if intervention_wave and i == intervention_wave - 1:
                    timeline_text += f"\n💊 **INTERVENTION APPLIED**\n"
                    if intervention_text:
                        preview = intervention_text[:100] + "..." if len(intervention_text) > 100 else intervention_text
                        timeline_text += f"  - {preview}\n"
                
                timeline_text += "\n"
            
            st.markdown(timeline_text)
    
    # Store for simulation
    questions = []  # Will be handled differently for longitudinal
    survey_context = ""
    response_validation = None

# Advanced settings (keep original)
with st.expander("⚙️ Advanced Settings"):
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
        max_tokens = st.slider(
            "Max Tokens",
            min_value=50,
            max_value=2000,
            value=st.session_state.default_max_tokens,
            step=50,
            help="Maximum response length"
        )

# Initialize optimization variables with defaults
enable_cache = True  # Always enable cache for better performance
enable_checkpoint = False
enable_parallel = False
max_workers = 1

st.markdown("---")

# Run simulation
st.subheader("4. Run Simulation")

# Validation
ready_to_run = False
if mode == "Survey":
    ready_to_run = len(selected_personas) > 0 and len(questions) > 0
elif mode == "Message Testing":
    ready_to_run = len(selected_personas) > 0 and intervention_text and len(questions) > 0
elif mode == "A/B Testing":
    ready_to_run = len(selected_personas) > 0 and len(conditions) >= 2 and len(questions) > 0
elif mode == "Longitudinal Study":
    ready_to_run = len(selected_personas) > 0 and len(waves_config) >= 2

if ready_to_run:
    total_queries = len(selected_personas) * len(questions)
    if mode == "Message Testing":
        total_queries += len(selected_personas)  # Add acknowledgment step
    
    # Enhanced simulation estimation
    st.markdown("### 📊 Simulation Plan")
    
    # Estimate time and cost
    avg_time_per_call = 3 if enable_parallel else 5  # seconds
    estimated_time_seconds = (total_queries * avg_time_per_call) / (max_workers if enable_parallel else 1)
    estimated_minutes = estimated_time_seconds / 60
    
    # Rough cost estimation (varies by model)
    api_provider = st.session_state.get('api_provider', 'Local (LM Studio)')
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
        parallel_status = "✅ Parallel" if enable_parallel else "Sequential"
        st.metric("Mode", parallel_status)
    
    # Tips based on settings
    if total_queries > 100 and not enable_parallel:
        st.warning("💡 **Tip:** Enable parallel processing for faster results with large simulations!")
    if total_queries > 50 and not enable_cache:
        st.info("💡 **Tip:** Enable caching to avoid re-running identical queries if you retry!")
    
    st.markdown("---")
    
    # Check if cloud API is being used
    api_provider = st.session_state.get('api_provider', 'Local (LM Studio)')
    supports_parallel = api_provider in ["DeepSeek", "OpenAI", "Custom OpenAI-Compatible"]
    
    # Parallel execution settings (for cloud APIs)
    if supports_parallel:
        col_p1, col_p2 = st.columns([1, 1])
        
        with col_p1:
            enable_parallel = st.checkbox(
                "⚡ Enable Parallel Execution",
                value=st.session_state.get('enable_parallel', False),
                help="Run multiple requests simultaneously for faster results (5-30x speedup)",
                key="sim_enable_parallel"
            )
        
        with col_p2:
            if enable_parallel:
                parallel_workers = st.slider(
                    "Concurrent Workers",
                    min_value=2,
                    max_value=20,
                    value=st.session_state.get('parallel_workers', 5),
                    help="Number of parallel requests. More workers = faster, but may hit rate limits.",
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
            st.info(f"⚡ Parallel mode enabled with {parallel_workers} workers - Expected speedup: ~{speedup}x")
        
        st.markdown("---")
    else:
        # Local API - no parallel support
        st.session_state.enable_parallel = False
        st.session_state.parallel_workers = 1
        st.info("💡 Switch to a cloud API (DeepSeek/OpenAI) in the homepage to enable parallel execution")
        st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        run_button = st.button("▶️ Run Simulation", type="primary", use_container_width=True)
    
    with col2:
        if 'simulation_running' in st.session_state and st.session_state.simulation_running:
            if st.button("⏹️ Stop", use_container_width=True, type="secondary"):
                st.session_state.stop_simulation = True
                st.session_state.simulation_running = False
                st.warning("⏹️ Stopping simulation... (may take a few seconds)")
    
    if run_button:
        st.session_state.simulation_running = True
        st.session_state.stop_simulation = False  # Reset stop flag
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Real-time log window
        st.markdown("---")
        st.markdown("### 📋 实时日志")
        log_container = st.container()
        with log_container:
            log_area = st.empty()
        
        # Initialize log list
        if 'simulation_logs' not in st.session_state:
            st.session_state.simulation_logs = []
        st.session_state.simulation_logs = []  # Clear previous logs
        
        def add_log(message: str, level: str = "INFO"):
            """Add a log message with timestamp"""
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Include milliseconds
            
            # Add emoji based on level
            emoji_map = {
                "INFO": "ℹ️",
                "SUCCESS": "✅",
                "WARNING": "⚠️",
                "ERROR": "❌",
                "REQUEST": "📤",
                "RESPONSE": "📥",
                "CACHE": "💾"
            }
            emoji = emoji_map.get(level, "📌")
            
            log_entry = f"[{timestamp}] {emoji} [{level:8s}] {message}"
            st.session_state.simulation_logs.append(log_entry)
            
            # Update log display (show last 30 logs with better formatting)
            recent_logs = st.session_state.simulation_logs[-30:]
            log_text = "\n".join(recent_logs)
            
            # Use markdown for better formatting with custom CSS
            log_area.markdown(
                f"""
                <div style="
                    background-color: #0e1117;
                    border: 1px solid #262730;
                    border-radius: 5px;
                    padding: 10px;
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                    color: #fafafa;
                    max-height: 400px;
                    overflow-y: auto;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                ">
{log_text}
                </div>
                """,
                unsafe_allow_html=True
            )
        
        results_container = st.container()
        
        # Add initial log
        add_log("Simulation initialized", "SUCCESS")
        
        # Initialize cache and checkpoint managers if enabled
        cache = None
        checkpoint_manager = None
        
        if enable_cache:
            from src import ResponseCache
            cache = ResponseCache(strategy='hybrid', max_memory_entries=1000)
            add_log("Response cache enabled (hybrid strategy)", "CACHE")
            status_text.text("✅ Cache enabled")
        
        if enable_checkpoint:
            from src import CheckpointManager
            checkpoint_manager = CheckpointManager()
            add_log("Auto-checkpoint enabled", "INFO")
            status_text.text("✅ Checkpoint manager enabled")
        
        # Create simulation engine with performance features
        engine = SimulationEngine(
            st.session_state.llm_client,
            cache=cache,
            checkpoint_manager=checkpoint_manager
        )
        
        add_log(f"Simulation engine initialized", "SUCCESS")
        
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
                st.info(f"🔧 Debug: Using parallel mode with {st.session_state.get('parallel_workers', 5)} workers")
            else:
                st.info(f"🔧 Debug: Using sequential mode (API: {api_provider})")
            
            if mode == "Survey":
                if use_parallel:
                    # Use parallel async execution for cloud APIs
                    import asyncio
                    import nest_asyncio
                    nest_asyncio.apply()  # Allow nested event loops in Streamlit
                    
                    from src import ParallelSimulationEngine
                    
                    add_log("Initializing parallel simulation engine", "INFO")
                    status_text.text("🔧 Initializing parallel engine...")
                    
                    parallel_engine = ParallelSimulationEngine(
                        llm_client=st.session_state.llm_client,
                        max_workers=st.session_state.get('parallel_workers', 5)
                    )
                    
                    workers = st.session_state.get('parallel_workers', 5)
                    total_requests = len(selected_personas) * len(questions)
                    add_log(f"Parallel mode: {workers} workers, {total_requests} total requests", "INFO")
                    status_text.text("🔧 Starting parallel execution...")
                    
                    # Function to check stop flag
                    def check_stop():
                        return st.session_state.get('stop_simulation', False)
                    
                    try:
                        with st.spinner(f"⚡ Running {len(selected_personas) * len(questions)} requests in parallel with {st.session_state.get('parallel_workers', 5)} workers..."):
                            # Get selected model
                            model = st.session_state.get('selected_model', None)
                            
                            add_log(f"Using model: {model}", "INFO")
                            status_text.text(f"🔧 Model: {model}, Personas: {len(selected_personas)}, Questions: {len(questions)}")
                            
                            # Create progress callback that checks stop flag
                            def progress_with_stop_check(msg):
                                if check_stop():
                                    parallel_engine.should_stop = True
                                    add_log("Stop signal received", "WARNING")
                                update_progress(msg)
                            
                            # Run async simulation
                            result = asyncio.run(parallel_engine.run_survey_parallel(
                                personas=selected_personas,
                                questions=questions,
                                temperature=temperature,
                                max_tokens=max_tokens,
                                progress_callback=progress_with_stop_check,
                                survey_context=survey_context if survey_context else None,
                                model=model,
                                response_validation=response_validation  # 添加响应格式验证
                            ))
                        
                        if check_stop():
                            add_log("Simulation stopped by user", "WARNING")
                            st.warning("⏹️ Simulation stopped by user")
                            st.session_state.simulation_running = False
                        else:
                            add_log(f"Parallel simulation complete! Collected {len(result.persona_responses)} responses", "SUCCESS")
                            status_text.text(f"✅ Parallel simulation complete! Got {len(result.persona_responses)} responses")
                    except asyncio.CancelledError:
                        add_log("Simulation cancelled by user", "WARNING")
                        st.warning("⏹️ Simulation cancelled by user")
                        st.session_state.simulation_running = False
                        st.stop()
                else:
                    # Sequential execution
                    add_log("Starting sequential survey execution", "INFO")
                    def check_stop():
                        return st.session_state.get('stop_simulation', False)
                    
                    try:
                        with st.spinner("Running survey simulation..."):
                            result = engine.run_survey(
                                personas=selected_personas,
                                questions=questions,
                                temperature=temperature,
                                max_tokens=max_tokens,
                                progress_callback=update_progress,
                                survey_context=survey_context if survey_context else None,
                                response_validation=response_validation,
                                survey_config=st.session_state.current_survey_config,
                                stop_callback=check_stop
                            )
                        
                        if check_stop():
                            add_log("Simulation stopped by user", "WARNING")
                            st.warning("⏹️ Simulation stopped by user")
                            st.session_state.simulation_running = False
                        else:
                            add_log("Sequential survey simulation complete", "SUCCESS")
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
                    import nest_asyncio
                    nest_asyncio.apply()
                    
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
                        with st.spinner(f"⚡ Running parallel message testing with {st.session_state.get('parallel_workers', 5)} workers..."):
                            model = st.session_state.get('selected_model', None)
                            
                            result = asyncio.run(parallel_engine.run_intervention_parallel(
                                personas=selected_personas,
                                intervention_text=intervention_text,
                                questions=questions,
                                temperature=temperature,
                                max_tokens=max_tokens,
                                progress_callback=progress_with_stop_check,
                                model=model
                            ))
                        
                        result.simulation_type = 'message_testing'
                        
                        if check_stop():
                            add_log("Simulation stopped by user", "WARNING")
                            st.warning("⏹️ Simulation stopped by user")
                            st.session_state.simulation_running = False
                        else:
                            add_log("Parallel message testing complete", "SUCCESS")
                            status_text.text("✅ Parallel message testing complete!")
                    except asyncio.CancelledError:
                        add_log("Simulation cancelled by user", "WARNING")
                        st.warning("⏹️ Simulation cancelled by user")
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
                                stop_callback=check_stop
                            )
                            result.simulation_type = 'message_testing'
                        
                        if check_stop():
                            add_log("Simulation stopped by user", "WARNING")
                            st.warning("⏹️ Simulation stopped by user")
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
                    import nest_asyncio
                    nest_asyncio.apply()
                    
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
                        
                        with st.spinner(f"⚡ Running parallel A/B test with {st.session_state.get('parallel_workers', 5)} workers..."):
                            model = st.session_state.get('selected_model', None)
                            
                            result = asyncio.run(parallel_engine.run_survey_parallel(
                                personas=selected_personas,
                                questions=questions,
                                temperature=temperature,
                                max_tokens=max_tokens,
                                progress_callback=progress_with_stop_check,
                                survey_context="A/B Test - Multiple Conditions",
                                model=model
                            ))
                        
                        result.simulation_type = 'ab_testing'
                        
                        if check_stop():
                            add_log("A/B test stopped by user", "WARNING")
                            st.warning("⏹️ A/B test stopped by user")
                            st.session_state.simulation_running = False
                        else:
                            add_log("Parallel A/B testing complete", "SUCCESS")
                            status_text.text("✅ Parallel A/B testing complete!")
                    except asyncio.CancelledError:
                        add_log("A/B test cancelled by user", "WARNING")
                        st.warning("⏹️ A/B test cancelled by user")
                        st.session_state.simulation_running = False
                        st.stop()
                else:
                    # Sequential A/B testing
                    add_log("Sequential A/B testing mode", "INFO")
                    with st.spinner("Running A/B test simulation..."):
                        result = engine.run_survey(
                            personas=selected_personas,
                            questions=questions,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            progress_callback=update_progress,
                            survey_context="A/B Test - Multiple Conditions"
                        )
                        result.simulation_type = 'ab_testing'
                    
                    if check_stop():
                        add_log("A/B test stopped by user", "WARNING")
                        st.warning("⏹️ A/B test stopped by user")
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
                status_text.text("🔄 Running longitudinal study...")
                
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
                            progress_callback=longitudinal_progress
                        )
                    
                    # Count total waves across all personas
                    total_waves = sum(len(wave_results) for wave_results in longitudinal_result.persona_results.values())
                    add_log(f"Longitudinal study complete! {total_waves} persona-waves executed", "SUCCESS")
                    
                    # Convert to standard SimulationResult format for storage
                    # Flatten all persona/wave responses
                    all_responses = []
                    for persona_name, wave_results in longitudinal_result.persona_results.items():
                        for wave_result in wave_results:
                            for response_item in wave_result.responses:
                                all_responses.append({
                                    'persona_name': persona_name,
                                    'question': f"[{wave_result.wave_name}] {response_item['question']}",
                                    'response': response_item['response'],
                                    'wave': wave_result.wave_name,
                                    'wave_number': wave_result.wave_number,
                                    'timestamp': response_item.get('timestamp', '')
                                })
                    
                    # Create SimulationResult object
                    from src.simulation import SimulationResult
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
                    
                    add_log(f"Created result with {len(all_responses)} total responses", "SUCCESS")
                    
                except Exception as e:
                    add_log(f"Longitudinal study error: {str(e)}", "ERROR")
                    import traceback
                    add_log(f"Traceback: {traceback.format_exc()[:500]}", "ERROR")
                    raise e
            
            progress_bar.progress(100)
            add_log("Simulation complete!", "SUCCESS")
            status_text.text("✅ Simulation complete!")
            
            # Show performance stats if available
            if cache or checkpoint_manager:
                stats = engine.get_performance_stats()
                
                add_log("Generating performance statistics", "INFO")
                
                perf_col1, perf_col2, perf_col3 = st.columns(3)
                
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
                
                with perf_col3:
                    if checkpoint_manager:
                        st.metric("Checkpoints Saved", "Auto", 
                                 help="Progress auto-saved every 50 responses")
                        add_log("Auto-checkpoint enabled during simulation", "INFO")
            
            # Save results
            add_log("Saving results to storage", "INFO")
            csv_file, json_file = st.session_state.results_storage.save_results(result)
            add_log(f"Results saved: {csv_file}", "SUCCESS")
            add_log(f"Results saved: {json_file}", "SUCCESS")
            
            st.success(f"✅ Simulation complete! Results saved to `{csv_file}` and `{json_file}`")
            
            # Display preview
            with results_container:
                st.subheader("📊 Results Preview")
                
                # Show summary
                st.write(f"**Personas:** {len(selected_personas)}")
                st.write(f"**Questions:** {len(questions)}")
                st.write(f"**Total Responses:** {len(result.persona_responses)}")
                
                add_log(f"Generated {len(result.persona_responses)} total responses", "SUCCESS")
                
                # Show sample responses
                with st.expander("View Sample Responses", expanded=True):
                    for i, response_data in enumerate(result.persona_responses[:5]):  # Show first 5
                        st.markdown(f"**{response_data['persona_name']}** - *{response_data['question']}*")
                        st.write(response_data['response'])
                        st.markdown("---")
                    
                    if len(result.persona_responses) > 5:
                        st.info(f"... and {len(result.persona_responses) - 5} more responses. View all in the Results page.")
                
                # Navigation button
                if st.button("📊 View Full Results", type="primary"):
                    st.switch_page("pages/3_Results.py")
        
        except Exception as e:
            add_log(f"EXCEPTION: {str(e)}", "ERROR")
            add_log(f"Exception type: {type(e).__name__}", "ERROR")
            st.error(f"❌ Error during simulation: {str(e)}")
            st.error(f"❌ Error type: {type(e).__name__}")
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
    st.info("👆 Please complete all required fields above to run the simulation")

# Footer
st.markdown("---")
st.caption("💡 Tip: Start with a small number of personas and questions to test your setup before running larger simulations.")
