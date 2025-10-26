"""Results page for viewing and analyzing simulation results."""
import streamlit as st
import pandas as pd
import json
from pathlib import Path
from src import ResultsStorage, SurveyScorer, render_navigation, render_system_status_badge
from src.styles import apply_global_styles

st.set_page_config(page_title="Results - LLM Simulation", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

# Apply global design system
apply_global_styles()

# Top Navigation
render_navigation(current_page="results")

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
        📊 Results Dashboard
    </h1>
    <p style="color: rgba(255,255,255,0.95); font-size: 1.1rem; line-height: 1.6; margin-bottom: 0;">
        Analyze simulation results, export data, and visualize insights from your AI-powered surveys.
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'results_storage' not in st.session_state:
    st.session_state.results_storage = ResultsStorage()

# Load all results
results_list = st.session_state.results_storage.list_results()

if not results_list:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    ">
        <h3 style="color: white; margin-top: 0;">📭 No Results Yet</h3>
        <p style="color: rgba(255,255,255,0.95); margin-bottom: 1rem;">
            Run a simulation from the Simulation page to see results here.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Go to Simulation →", type="primary"):
        st.switch_page("pages/2_Simulation.py")
    st.stop()

# Dashboard Overview Cards
st.markdown("""
<div style="
    background: white;
    border-left: 4px solid #667eea;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
">
    <h3 style="color: #667eea; font-size: 1.3rem; margin: 0;">📈 Overview</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# Calculate stats
survey_count = sum(1 for r in results_list if r['type'] == 'survey')
intervention_count = sum(1 for r in results_list if r['type'] in ['message_testing', 'ab_testing', 'intervention'])

# Count total responses
total_responses = 0
for result in results_list:
    try:
        csv_data = st.session_state.results_storage.load_csv_result(result['csv_file'])
        if csv_data is not None:
            total_responses += len(csv_data)
    except:
        pass

with col1:
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
    ">
        <div style="font-size: 2.5rem; font-weight: 700; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;">
            {len(results_list)}
        </div>
        <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
            Total Simulations
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
    ">
        <div style="font-size: 2.5rem; font-weight: 700; color: #4caf50;">
            {survey_count}
        </div>
        <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
            Survey Results
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
    ">
        <div style="font-size: 2.5rem; font-weight: 700; color: #2196f3;">
            {intervention_count}
        </div>
        <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
            Intervention Tests
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
    ">
        <div style="font-size: 2.5rem; font-weight: 700; color: #ff9800;">
            {total_responses}
        </div>
        <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
            Total Responses
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# Result selection
st.subheader(f"📋 Select Result to Analyze")

# Add quick filter
col_filter1, col_filter2 = st.columns([1, 3])
with col_filter1:
    result_type_filter = st.selectbox(
        "Filter by type:",
        ["All Types", "Survey", "Message Testing", "A/B Testing"],
        key="type_filter"
    )

# Filter results based on selection
if result_type_filter != "All Types":
    type_map = {
        "Survey": "survey",
        "Message Testing": ["message_testing", "intervention"],
        "A/B Testing": "ab_testing"
    }
    filter_types = type_map[result_type_filter]
    if isinstance(filter_types, list):
        filtered_results = [r for r in results_list if r['type'] in filter_types]
    else:
        filtered_results = [r for r in results_list if r['type'] == filter_types]
else:
    filtered_results = results_list

if not filtered_results:
    st.warning(f"No {result_type_filter} results found. Try a different filter.")
    st.stop()

# Add emoji indicators for different types
def format_result_name(result):
    type_emoji = {
        'survey': '📋',
        'message_testing': '💬',
        'intervention': '💬',
        'ab_testing': '🧪'
    }
    emoji = type_emoji.get(result['type'], '📊')
    type_label = result['type'].replace('_', ' ').title()
    return f"{emoji} {result['name']} - {type_label} ({result['modified']})"

with col_filter2:
    selected_result = st.selectbox(
        "Choose a simulation:",
        filtered_results,
        format_func=format_result_name,
        key="result_selector"
    )

if not selected_result:
    st.stop()

st.markdown("---")

# Create tabs for different views
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Overview", "📊 Data Table", "🎯 Instrument Scores", "💬 Detailed Responses", "📥 Export"])

# Load the selected result
csv_data = st.session_state.results_storage.load_csv_result(selected_result['csv_file'])
json_data = st.session_state.results_storage.load_json_result(selected_result['json_file'])

# Tab 1: Overview
with tab1:
    st.header("Simulation Overview")
    
    if json_data:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Format simulation type for display
            sim_type = json_data['simulation_type']
            if sim_type == 'message_testing':
                display_type = "Message Testing"
            elif sim_type == 'ab_testing':
                display_type = "A/B Testing"
            elif sim_type == 'survey_parallel':
                display_type = "Survey (Parallel)"
            elif sim_type == 'longitudinal_intervention':
                display_type = "Longitudinal Study"
            else:
                display_type = sim_type.title()
            
            st.metric("Simulation Type", display_type)
            st.metric("Timestamp", json_data['timestamp'].split('T')[0])
        
        with col2:
            num_personas = len(set([r['persona_name'] for r in json_data['responses']]))
            st.metric("Personas", num_personas)
            st.metric("Questions", len(json_data['questions']))
        
        with col3:
            st.metric("Total Responses", len(json_data['responses']))
            
            # Show specific metrics based on simulation type
            if sim_type == 'message_testing':
                if 'intervention_text' in json_data:
                    st.metric("Message/Intervention", "Present")
                else:
                    st.metric("Message/Intervention", "Not Found")
            elif sim_type == 'ab_testing':
                if 'ab_test_conditions' in json_data:
                    st.metric("Conditions", len(json_data['ab_test_conditions']))
                else:
                    st.metric("A/B Test", "Basic Mode")
            elif 'intervention_text' in json_data:
                st.metric("Intervention", "Yes")
            else:
                st.metric("Intervention", "No")
        
        # Show simulation-specific content
        if sim_type == 'message_testing' and 'intervention_text' in json_data:
            st.markdown("---")
            st.subheader("� Message/Intervention Presented to Personas")
            with st.container():
                st.markdown("""
                <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #1e90ff;">
                """, unsafe_allow_html=True)
                st.markdown(json_data['intervention_text'])
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("---")
        
        elif sim_type == 'ab_testing' and 'ab_test_conditions' in json_data:
            st.subheader("🧪 A/B Test Conditions")
            for i, condition in enumerate(json_data['ab_test_conditions'], 1):
                st.write(f"**Condition {i}:** {condition}")
            st.markdown("---")
        
        # Show questions
        st.subheader("Questions Asked")
        for i, question in enumerate(json_data['questions'], 1):
            st.write(f"{i}. {question}")
        
        # Show intervention if applicable
        if json_data['intervention_text']:
            st.subheader("Intervention Text")
            st.info(json_data['intervention_text'])
        
        # Persona summary
        st.subheader("Participating Personas")
        persona_names = sorted(set([r['persona_name'] for r in json_data['responses']]))
        
        cols = st.columns(min(3, len(persona_names)))
        for i, name in enumerate(persona_names):
            with cols[i % 3]:
                # Get persona details from first response
                persona_data = next(r for r in json_data['responses'] if r['persona_name'] == name)
                st.write(f"**{name}**")
                st.write(f"Age: {persona_data['persona_age']}")
                st.write(f"Occupation: {persona_data['persona_occupation']}")

# Tab 2: Data Table
with tab2:
    st.header("Response Data")
    
    if csv_data is not None:
        # Display filters
        st.subheader("Filters")
        col1, col2 = st.columns(2)
        
        with col1:
            # Filter by persona
            all_personas = csv_data['persona_name'].unique().tolist()
            selected_personas = st.multiselect(
                "Filter by Persona",
                all_personas,
                default=all_personas,
                key="persona_filter"
            )
        
        with col2:
            # Filter by question
            all_questions = csv_data['question'].unique().tolist()
            selected_questions = st.multiselect(
                "Filter by Question",
                all_questions,
                default=all_questions,
                key="question_filter"
            )
        
        # Apply filters
        filtered_data = csv_data[
            (csv_data['persona_name'].isin(selected_personas)) &
            (csv_data['question'].isin(selected_questions))
        ]
        
        st.write(f"Showing {len(filtered_data)} of {len(csv_data)} responses")
        
        # Add view format option
        view_format = st.radio(
            "Data Format:",
            ["Long Format (one row per response)", "Wide Format (questions as columns)"],
            horizontal=True,
            help="Long format: each row is a question-response pair. Wide format: each row is a persona with questions as columns.",
            key="data_format_radio"
        )
        
        if view_format == "Long Format (one row per response)":
            # Display table in long format
            st.dataframe(
                filtered_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "response": st.column_config.TextColumn(
                        "Response",
                        width="large"
                    )
                }
            )
        else:
            # Wide format: pivot questions into columns
            st.info("📋 Wide format: Each row is a persona, each column is a question")
            
            # Create pivot table
            wide_data = filtered_data.pivot_table(
                index=['persona_name', 'persona_age', 'persona_occupation'],
                columns='question',
                values='response',
                aggfunc='first'
            ).reset_index()
            
            # Rename columns for clarity
            wide_data.columns.name = None
            wide_data = wide_data.rename(columns={
                'persona_name': 'Name',
                'persona_age': 'Age',
                'persona_occupation': 'Occupation'
            })
            
            st.write(f"Showing {len(wide_data)} personas × {len(filtered_data['question'].unique())} questions")
            
            # Display with horizontal scroll
            st.dataframe(wide_data, use_container_width=True, hide_index=True)
            
            # Download button for wide format
            st.download_button(
                label="⬇️ Download Wide Format CSV",
                data=wide_data.to_csv(index=False),
                file_name=f"survey_wide_{selected_result['name']}.csv",
                mime="text/csv",
                help="Download wide-format table (perfect for Excel, SPSS, R, etc.)"
            )
        
        # Basic statistics
        with st.expander("📈 Basic Statistics"):
            st.write("**Response Length Statistics**")
            
            # Calculate response lengths (convert to string first to handle any non-string values)
            filtered_data['response_length'] = filtered_data['response'].astype(str).str.len()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Average Length", f"{filtered_data['response_length'].mean():.0f} chars")
            with col2:
                st.metric("Median Length", f"{filtered_data['response_length'].median():.0f} chars")
            with col3:
                st.metric("Min Length", f"{filtered_data['response_length'].min():.0f} chars")
            with col4:
                st.metric("Max Length", f"{filtered_data['response_length'].max():.0f} chars")
            
            # Response lengths by persona
            st.write("**Average Response Length by Persona**")
            persona_avg = filtered_data.groupby('persona_name')['response_length'].mean().sort_values(ascending=False)
            st.bar_chart(persona_avg)
        
        # A/B Testing specific analysis
        if json_data and json_data.get('simulation_type') == 'ab_testing' and 'ab_test_assignments' in json_data:
            with st.expander("🧪 A/B Test Analysis"):
                st.subheader("Condition Comparison")
                
                # Create condition analysis
                assignments = json_data['ab_test_assignments']
                condition_analysis = {}
                
                for persona_name, condition_id in assignments.items():
                    if condition_id not in condition_analysis:
                        condition_analysis[condition_id] = []
                    
                    # Find responses for this persona
                    persona_responses = filtered_data[filtered_data['persona_name'] == persona_name]
                    if not persona_responses.empty:
                        condition_analysis[condition_id].extend(persona_responses['response_length'].tolist())
                
                # Display condition comparison
                if condition_analysis:
                    condition_stats = []
                    for condition_id, lengths in condition_analysis.items():
                        if lengths:
                            condition_name = condition_id  # Simplified for now
                            condition_stats.append({
                                'Condition': condition_name,
                                'Count': len(lengths),
                                'Avg Length': f"{sum(lengths)/len(lengths):.1f}",
                                'Min Length': min(lengths),
                                'Max Length': max(lengths)
                            })
                    
                    if condition_stats:
                        import pandas as pd
                        stats_df = pd.DataFrame(condition_stats)
                        st.dataframe(stats_df, use_container_width=True)
                        
                        # Simple comparison
                        if len(condition_stats) >= 2:
                            st.subheader("📈 Condition Comparison")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                best_condition = max(condition_stats, key=lambda x: float(x['Avg Length']))
                                st.success(f"**Longest Responses:** {best_condition['Condition']} ({best_condition['Avg Length']} chars avg)")
                            
                            with col2:
                                shortest_condition = min(condition_stats, key=lambda x: float(x['Avg Length']))
                                st.info(f"**Shortest Responses:** {shortest_condition['Condition']} ({shortest_condition['Avg Length']} chars avg)")
        
        # Message Testing specific analysis
        elif json_data and json_data.get('simulation_type') == 'message_testing':
            with st.expander("💬 Message Testing Analysis"):
                st.subheader("Response Patterns")
                
                # Group by persona to see individual patterns
                persona_groups = filtered_data.groupby('persona_name')
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Most Responsive Persona", persona_groups['response_length'].mean().idxmax())
                    st.metric("Least Responsive Persona", persona_groups['response_length'].mean().idxmin())
                
                with col2:
                    st.metric("Most Consistent Persona", persona_groups['response_length'].std().idxmin())
                    st.metric("Most Variable Persona", persona_groups['response_length'].std().idxmax())
                
                # Show top responses - using columns instead of nested expander
                st.subheader("📝 Sample Responses")
                sample_responses = filtered_data.nlargest(5, 'response_length')
                for idx, row in sample_responses.iterrows():
                    st.markdown(f"**{row['persona_name']}** - {row['response_length']} chars")
                    st.write(f"**Q:** {row['question']}")
                    st.write(f"**A:** {row['response']}")
                    st.markdown("---")

# Tab 3: Instrument Scores
with tab3:
    st.header("Instrument Scores & Analysis")
    
    # Check if this is a standardized instrument
    instrument_name = json_data.get('instrument_name') if json_data else None
    
    if instrument_name:
        st.info(f"📊 Standardized Instrument Detected: **{instrument_name}**")
        
        # Try to calculate scores
        try:
            # Get responses in wide format for scoring
            if csv_data is not None and not csv_data.empty:
                scores_df = SurveyScorer.calculate_scores_for_personas(csv_data, instrument_name)
                
                if not scores_df.empty:
                    st.success(f"✅ Calculated scores for {len(scores_df)} personas")
                    
                    # Display score statistics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Mean Score", f"{scores_df['total_score'].mean():.1f}")
                    with col2:
                        st.metric("Median Score", f"{scores_df['total_score'].median():.1f}")
                    with col3:
                        st.metric("Std Dev", f"{scores_df['total_score'].std():.1f}")
                    with col4:
                        clinical_pct = (scores_df['clinical_cutoff'].sum() / len(scores_df)) * 100
                        st.metric("Clinical %", f"{clinical_pct:.1f}%")
                    
                    st.markdown("---")
                    
                    # Score distribution
                    st.subheader("Score Distribution by Severity")
                    severity_counts = scores_df['severity'].value_counts()
                    st.bar_chart(severity_counts)
                    
                    st.markdown("---")
                    
                    # Individual scores table
                    st.subheader("Individual Persona Scores")
                    display_df = scores_df[['persona_name', 'total_score', 'severity', 'interpretation', 'clinical_cutoff']]
                    display_df = display_df.rename(columns={
                        'persona_name': 'Persona',
                        'total_score': 'Score',
                        'severity': 'Severity',
                        'interpretation': 'Interpretation',
                        'clinical_cutoff': 'Clinical'
                    })
                    
                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Clinical": st.column_config.CheckboxColumn("Clinical")
                        }
                    )
                    
                    # Download scores
                    st.download_button(
                        label="⬇️ Download Scores CSV",
                        data=scores_df.to_csv(index=False),
                        file_name=f"scores_{instrument_name}_{selected_result['name']}.csv",
                        mime="text/csv",
                        help="Download detailed scores with all metadata"
                    )
                else:
                    st.warning("Could not calculate scores. Responses may not be numeric.")
            else:
                st.warning("No data available for scoring.")
        except Exception as e:
            st.error(f"Error calculating scores: {str(e)}")
    else:
        st.info("📝 This appears to be a custom survey (no standardized instrument detected).")
        st.write("Automated scoring is only available for standardized instruments like PHQ-9, GAD-7, PSS-10, and WHO-5.")
        st.write("You can still view all responses in the other tabs.")

# Tab 4: Detailed Responses
with tab4:
    st.header("Detailed Response Viewer")
    
    if json_data:
        # Group responses by question or persona
        view_by = st.radio("View by:", ["Question", "Persona"], horizontal=True)
        
        if view_by == "Question":
            # Group by question
            for question in json_data['questions']:
                st.subheader(f"Q: {question}")
                
                question_responses = [r for r in json_data['responses'] if r['question'] == question]
                
                for response_data in question_responses:
                    with st.expander(f"**{response_data['persona_name']}** ({response_data['persona_occupation']})"):
                        st.write(response_data['response'])
                        
                        # Show conversation history if available (not nested)
                        if response_data.get('conversation_history'):
                            st.markdown("---")
                            st.markdown("**💬 Conversation History:**")
                            for msg in response_data['conversation_history']:
                                if msg['role'] == 'system':
                                    st.caption(f"**System:** {msg['content'][:200]}...")
                                elif msg['role'] == 'user':
                                    st.info(f"**User:** {msg['content']}")
                                else:
                                    st.success(f"**Assistant:** {msg['content']}")
                
                st.markdown("---")
        
        else:  # View by Persona
            persona_names = sorted(set([r['persona_name'] for r in json_data['responses']]))
            
            for persona_name in persona_names:
                persona_responses = [r for r in json_data['responses'] if r['persona_name'] == persona_name]
                
                # Get persona details
                first_response = persona_responses[0]
                st.subheader(f"{persona_name}")
                st.caption(f"{first_response['persona_age']} years old, {first_response['persona_occupation']}")
                
                for response_data in persona_responses:
                    with st.expander(f"**Q:** {response_data['question']}"):
                        st.write(response_data['response'])
                
                st.markdown("---")

# Tab 5: Export
with tab5:
    st.header("Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 CSV Export")
        st.write("Flat format suitable for spreadsheet analysis")
        
        if csv_data is not None:
            csv_string = csv_data.to_csv(index=False)
            
            st.download_button(
                label="⬇️ Download CSV",
                data=csv_string,
                file_name=selected_result['csv_file'],
                mime="text/csv",
                use_container_width=True
            )
            
            st.info(f"File: {selected_result['csv_file']}\nSize: {len(csv_data)} rows")
    
    with col2:
        st.subheader("📋 JSON Export")
        st.write("Detailed format including conversation history")
        
        if json_data:
            json_string = json.dumps(json_data, indent=2)
            
            st.download_button(
                label="⬇️ Download JSON",
                data=json_string,
                file_name=selected_result['json_file'],
                mime="application/json",
                use_container_width=True
            )
            
            st.info(f"File: {selected_result['json_file']}\nSize: {len(json_string)} bytes")
    
    # Special export options for Message Testing and A/B Testing
    if json_data and json_data.get('simulation_type') in ['message_testing', 'ab_testing']:
        st.markdown("---")
        
        if json_data.get('simulation_type') == 'message_testing':
            st.subheader("💬 Message Testing Export")
            
            if 'intervention_text' in json_data:
                st.write("**Message/Intervention Text:**")
                st.text_area("Intervention Text", json_data['intervention_text'], height=100, disabled=True)
                
                # Export intervention text separately
                st.download_button(
                    label="📝 Download Intervention Text",
                    data=json_data['intervention_text'],
                    file_name=f"intervention_{selected_result['csv_file'].replace('.csv', '.txt')}",
                    mime="text/plain",
                    use_container_width=True
                )
        
        elif json_data.get('simulation_type') == 'ab_testing':
            st.subheader("🧪 A/B Testing Export")
            
            if 'ab_test_conditions' in json_data:
                st.write("**Test Conditions:**")
                for i, condition in enumerate(json_data['ab_test_conditions'], 1):
                    st.write(f"{i}. {condition}")
                
                # Export A/B test configuration
                ab_config = {
                    'test_type': 'A/B Testing',
                    'conditions': json_data['ab_test_conditions'],
                    'assignments': json_data.get('ab_test_assignments', {}),
                    'questions': json_data.get('questions', []),
                    'timestamp': json_data.get('timestamp', '')
                }
                
                st.download_button(
                    label="🧪 Download A/B Test Configuration",
                    data=json.dumps(ab_config, indent=2),
                    file_name=f"ab_test_config_{selected_result['csv_file'].replace('.csv', '.json')}",
                    mime="application/json",
                    use_container_width=True
                )
    
    # Text Analysis & Word Cloud - Available for ALL result types
    st.markdown("---")
    st.subheader("🔎 Text Analysis & Word Cloud")
    st.caption("Export and visualize responses for any question")

    # Per-question export
    if csv_data is not None:
        questions = csv_data['question'].unique().tolist()
        qsel = st.selectbox("Select question for export/visualization:", questions, key="wc_question_select")

        # Filter responses for selected question
        q_responses = csv_data[csv_data['question'] == qsel]['response'].astype(str).tolist()

        # Provide raw export options
        combined_text = "\n\n".join(q_responses)
        st.download_button(
            label="⬇️ Download Raw Responses (TXT)",
            data=combined_text,
            file_name=f"responses_{qsel[:30].replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        # Escape quotes for CSV format
        csv_rows = []
        for r in q_responses:
            escaped = r.replace('"', '""')
            csv_rows.append(f'"{escaped}"')
        
        st.download_button(
            label="⬇️ Download Responses (CSV)",
            data="\n".join(csv_rows),
            file_name=f"responses_{qsel[:30].replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True
        )

        # Word cloud generation (try to import & handle missing libs)
        try:
            from wordcloud import WordCloud
            wordcloud_available = True
        except Exception as e:
            wordcloud_available = False
            import_error = str(e)

        # Check for Chinese segmentation if needed
        requires_jieba = False
        sample_text = combined_text
        # crude check for Chinese characters
        if any('\u4e00' <= ch <= '\u9fff' for ch in sample_text):
            requires_jieba = True
            try:
                import jieba  # type: ignore
                jieba_available = True
            except Exception:
                jieba_available = False

        if not wordcloud_available:
            st.warning(f"WordCloud library not installed. Install `wordcloud` to enable visualizations (pip install wordcloud). You can still download raw text.")
            if 'import_error' in locals():
                st.error(f"Import error details: {import_error}")
        else:
            # Prepare text (segment Chinese if necessary)
            if requires_jieba and not jieba_available:
                st.warning("Detected Chinese text. Install `jieba` for better segmentation (pip install jieba) to enable word cloud for Chinese.")
            if st.button("🔮 Generate Word Cloud", key="generate_wc"):
                # Create cleaned text
                text_for_wc = " ".join(q_responses)
                if requires_jieba and jieba_available:
                    import jieba  # type: ignore
                    text_for_wc = " ".join(jieba.lcut(text_for_wc))

                wc = WordCloud(width=800, height=400, background_color='white').generate(text_for_wc)

                # Display image
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wc, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
    
    st.markdown("---")
    
    # Delete option
    st.subheader("🗑️ Delete Results")
    st.warning("This action cannot be undone!")
    
    if st.button("Delete This Result", type="secondary"):
        confirm = st.checkbox("I confirm I want to delete this result")
        
        if confirm:
            if st.button("⚠️ Confirm Delete", type="primary"):
                base_name = selected_result['name']
                if st.session_state.results_storage.delete_result(base_name):
                    st.success("Result deleted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to delete result")

# Footer
st.markdown("---")
st.caption("💡 Tip: Export results to CSV for further analysis in spreadsheet software or statistical tools.")

