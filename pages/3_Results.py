"""Results page for viewing and analyzing simulation results."""
import streamlit as st
import pandas as pd
import json
from pathlib import Path
from src import (ResultsStorage, results_to_wide, SurveyScorer, render_navigation, render_page_header, section, stat_cards,
                 render_empty_state, question_collapse_report, cronbach_alpha,
                 distribution_divergence, ABTestManager)
from src.styles import apply_global_styles


def _benjamini_hochberg(p_values):
    """Return FDR-adjusted q-values in the original order."""
    n = len(p_values)
    if not n:
        return []
    order = sorted(range(n), key=lambda i: p_values[i])
    adjusted = [1.0] * n
    running = 1.0
    for rank_index in range(n - 1, -1, -1):
        original_index = order[rank_index]
        rank = rank_index + 1
        running = min(running, float(p_values[original_index]) * n / rank)
        adjusted[original_index] = min(1.0, running)
    return adjusted


st.set_page_config(page_title="Results - LLM Simulation", page_icon="A", layout="wide", initial_sidebar_state="collapsed")

# Apply global design system
apply_global_styles()

# Top Navigation
render_navigation(current_page="results")

render_page_header(
    "Results workspace",
    "Inspect response quality, compare runs, estimate condition effects, and export a reproducible record.",
    eyebrow="Analysis",
)

# Initialize session state
if 'results_storage' not in st.session_state:
    st.session_state.results_storage = ResultsStorage()

# Load all results (metadata from JSON sidecars — no CSV parsing here)
results_list = st.session_state.results_storage.list_results()

if not results_list:
    render_empty_state(
        "No simulation results",
        "Completed studies will appear here with quality checks, comparisons, and export options.",
        icon="◇",
    )
    if st.button("Go to Simulation →", type="primary"):
        st.switch_page("pages/2_Simulation.py")
    st.stop()

# Overview stats (from list_results metadata; n_responses missing for legacy files)
survey_count = sum(1 for r in results_list if r['type'] == 'survey')
intervention_count = sum(1 for r in results_list if r['type'] in ['message_testing', 'ab_testing', 'intervention'])
total_responses = sum(r.get('n_responses', 0) for r in results_list)
stat_cards([
    ("Simulations", len(results_list)),
    ("Surveys", survey_count),
    ("Intervention Tests", intervention_count),
    ("Responses", total_responses),
])

# ---- Selection + clear-all ----
@st.dialog("Delete all results?")
def confirm_clear_all():
    st.write("This permanently deletes every simulation result. It cannot be undone.")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Delete all", type="primary", use_container_width=True):
            deleted_count, error_count = st.session_state.results_storage.clear_all_results()
            st.toast(f"Deleted {deleted_count} files" + (f" ({error_count} errors)" if error_count else ""))
            st.rerun()
    with c2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()

col_header, col_clear = st.columns([3, 1])
with col_header:
    section("Select a run", first=True)
with col_clear:
    if st.button("Clear all", use_container_width=True):
        confirm_clear_all()

col_filter1, col_filter2 = st.columns([1, 3])
with col_filter1:
    result_type_filter = st.selectbox(
        "Filter by type",
        ["All Types", "Survey", "Message Testing", "A/B Testing", "Longitudinal"],
        key="type_filter"
    )

if result_type_filter != "All Types":
    type_map = {
        "Survey": "survey",
        "Message Testing": ["message_testing", "intervention"],
        "A/B Testing": "ab_testing",
        "Longitudinal": "longitudinal",
    }
    filter_types = type_map[result_type_filter]
    if isinstance(filter_types, list):
        filtered_results = [r for r in results_list if r['type'] in filter_types]
    else:
        filtered_results = [r for r in results_list if r['type'] == filter_types]
else:
    filtered_results = results_list

if not filtered_results:
    st.caption(f"No {result_type_filter} runs yet — pick another type, or run one on the Simulation page.")
    st.stop()

def format_result_name(result):
    label = result['type'].replace('_', ' ').title()
    return f"{result['name']} · {label} · {result['modified']}"

with col_filter2:
    selected_result = st.selectbox(
        "Choose a simulation",
        filtered_results,
        format_func=format_result_name,
        key="result_selector"
    )

if not selected_result:
    st.stop()

# ---- Compare runs ----
with st.expander("Compare runs (select 2+)"):
    compare_picks = st.multiselect(
        "Runs to compare",
        results_list,
        format_func=format_result_name,
        key="compare_selector"
    )
    if len(compare_picks) >= 2:
        # Per-run summary
        summary_rows = []
        for r in compare_picks:
            summary_rows.append({
                'run': r['name'], 'type': r['type'],
                'model': r.get('model', ''), 'seed': r.get('seed', ''),
                'questions': r.get('n_questions', ''), 'responses': r.get('n_responses', ''),
                'modified': r['modified'],
            })
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

        # Per-question modal share across runs sharing questions
        share_tables = []
        for r in compare_picks:
            df = st.session_state.results_storage.load_csv_result(r['csv_file'])
            if df is None or df.empty:
                continue
            rep = question_collapse_report(df)[['question', 'modal_answer', 'modal_share', 'collapsed']]
            rep = rep.rename(columns={'modal_answer': f'{r["name"]} · modal', 'modal_share': f'{r["name"]} · share', 'collapsed': f'{r["name"]} · collapsed'})
            share_tables.append(rep)
        if len(share_tables) >= 2:
            merged = share_tables[0]
            for t in share_tables[1:]:
                merged = merged.merge(t, on='question', how='outer')
            st.markdown("**Per-question answer concentration (shared questions)**")
            st.dataframe(merged, use_container_width=True, hide_index=True)

        # A/B stats for runs with a condition column
        for r in compare_picks:
            df = st.session_state.results_storage.load_csv_result(r['csv_file'])
            if df is None or 'condition' not in df.columns or df['condition'].fillna('').eq('').all():
                continue
            rows = []
            mgr = ABTestManager()
            for q, grp in df.groupby('question'):
                grp = grp.assign(_num=pd.to_numeric(grp['response'], errors='coerce')).dropna(subset=['_num'])
                by_cond = {c: g['_num'].tolist() for c, g in grp.groupby('condition') if len(g) >= 2}
                if len(by_cond) < 2:
                    continue
                stats = mgr.compare_conditions(by_cond)
                if 'error' in stats:
                    continue
                rows.append({'question': q, 'test': stats['test'], 'statistic': round(stats['statistic'], 3),
                             'p_value': stats['p_value'], 'effect_size': round(stats['effect_size'], 3)})
            if rows:
                q_values = _benjamini_hochberg([row['p_value'] for row in rows])
                for row, q_value in zip(rows, q_values):
                    row['p_value'] = round(row['p_value'], 4)
                    row['q_value_fdr'] = round(q_value, 4)
                    row['significant_fdr'] = q_value < 0.05
                st.markdown(f"**A/B condition effects — {r['name']}**")
                st.caption("Welch tests with Benjamini–Hochberg correction across questions.")
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.markdown("---")

# Create tabs for different views
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Data Table", "Instrument Scores", "Detailed Responses", "Export"])

# Load the selected result
csv_data = st.session_state.results_storage.load_csv_result(selected_result['csv_file'])
json_data = st.session_state.results_storage.load_json_result(selected_result['json_file'])

with tab1:

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
            st.markdown("**Message/Intervention Presented to Personas**")
            st.info(json_data.get('intervention_text'))
            st.markdown("---")


        elif sim_type == 'ab_testing' and 'ab_test_conditions' in json_data:
            st.markdown("**A/B Test Conditions**")
            for i, condition in enumerate(json_data['ab_test_conditions'], 1):
                st.write(f"**Condition {i}:** {condition}")
            st.markdown("---")

        # Show questions
        st.markdown("**Questions Asked**")
        for i, question in enumerate(json_data['questions'], 1):
            st.write(f"{i}. {question}")

        # Show intervention if applicable
        if json_data.get('intervention_text'):
            st.markdown("**Intervention Text**")
            st.info(json_data.get('intervention_text'))

        # Validity panel: distribution-collapse check + run metadata
        resp_df = pd.DataFrame([{
            'question': r['question'],
            'response': r['response'],
            'validation_status': r.get('validation_status', 'not_requested'),
        } for r in json_data['responses']])
        if not resp_df.empty:
            report = question_collapse_report(resp_df)
            n_collapsed = int(report['collapsed'].sum())
            with st.expander(f"Validity Check — {n_collapsed}/{len(report)} questions collapsed",
                             expanded=n_collapsed > 0):
                meta = json_data.get('metadata') or {}
                if meta.get('model') or meta.get('seed') is not None:
                    st.caption(f"model: {meta.get('model', '?')} · seed: {meta.get('seed', 'not fixed')}")
                if n_collapsed > 0:
                    st.warning(f"{n_collapsed} question(s) have ≥85% identical answers — synthetic respondents "
                               "collapsed onto one answer. Consider enabling 'Reduce Answer Collapse' in "
                               "Advanced Settings or raising temperature.")
                st.dataframe(report, use_container_width=True)

            # Human-reference divergence (silicon-sampling benchmark practice)
            with st.expander("Compare against a human reference distribution"):
                st.caption("Paste a real-survey answer distribution to see how far the simulation is from humans. "
                           "Format: `answer:share` separated by commas, e.g. `yes:0.6, no:0.4`")
                ref_q = st.selectbox("Question", report['question'].tolist(), key="ref_div_q")
                ref_text = st.text_input("Reference distribution", key="ref_div_text",
                                         placeholder="yes:0.6, no:0.4")
                if ref_text:
                    try:
                        ref = {k.strip(): float(v) for k, v in
                               (part.split(':') for part in ref_text.split(','))}
                        obs = resp_df.loc[resp_df['question'] == ref_q, 'response']
                        div = distribution_divergence(obs, ref)
                        c1, c2, c3 = st.columns(3)
                        c1.metric("TVD", div['tvd'], help="Total variation distance: 0 = identical, 1 = disjoint")
                        c2.metric("JSD", div['jsd'], help="Jensen-Shannon divergence (bits): 0 = identical, 1 = max")
                        c3.metric("Coverage", div['coverage'],
                                  help="Share of simulated answers that exist in the reference; <1 means off-scale answers")
                    except (ValueError, ZeroDivisionError):
                        st.error("Could not parse — use `answer:share, answer:share` with numeric shares.")

        # Persona summary
        st.markdown("**Participating Personas**")
        persona_names = sorted(set([r['persona_name'] for r in json_data['responses']]))

        if persona_names:
            cols = st.columns(min(3, len(persona_names)))
            for i, name in enumerate(persona_names):
                with cols[i % len(cols)]:
                    # Get persona details from first response
                    persona_data = next(r for r in json_data['responses'] if r['persona_name'] == name)
                    st.write(f"**{name}**")
                    st.write(f"Age: {persona_data.get('persona_age', '—')}")
                    st.write(f"Occupation: {persona_data.get('persona_occupation', '—')}")
        else:
            st.caption("No completed persona responses in this run.")

# Tab 2: Data Table
with tab2:
    if csv_data is not None:
        # Display filters
        st.markdown("**Filters**")
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

        # Subgroup breakdown (stratified fidelity check, RSS-style)
        with st.expander("Breakdown by subgroup"):
            sc1, sc2 = st.columns(2)
            with sc1:
                sub_q = st.selectbox("Question", all_questions, key="subgroup_q")
            with sc2:
                sub_dim = st.selectbox("Subgroup by", ["Gender", "Age group"], key="subgroup_dim")
            sub_df = filtered_data[filtered_data['question'] == sub_q].copy()
            if not sub_df.empty:
                if sub_dim == "Age group":
                    sub_df['_grp'] = pd.cut(pd.to_numeric(sub_df.get('persona_age', '—'), errors='coerce'),
                                            bins=[0, 29, 44, 59, 150], labels=['18-29', '30-44', '45-59', '60+'])
                else:
                    sub_df['_grp'] = sub_df.get('persona_gender', '—')
                ct = pd.crosstab(sub_df['_grp'], sub_df['response'].astype(str), normalize='index').round(2)
                st.dataframe(ct, use_container_width=True)
                st.caption("Row-normalized answer shares per subgroup. Flat rows = persona conditioning added no signal.")

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
            st.info("One row per persona: complete persona_* variables first, followed by one answer__ column per question.")
            wide_data = results_to_wide(filtered_data)

            st.write(f"Showing {len(wide_data)} personas × {len(filtered_data['question'].unique())} questions")

            # Display with horizontal scroll
            st.dataframe(wide_data, use_container_width=True, hide_index=True)

            # Download button for wide format
            st.download_button(
                label="Download Wide Format CSV",
                data=wide_data.to_csv(index=False),
                file_name=f"survey_wide_{selected_result['name']}.csv",
                mime="text/csv",
                help="Download wide-format table (perfect for Excel, SPSS, R, etc.)"
            )

        # Basic statistics
        with st.expander("Basic Statistics"):
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
            with st.expander("A/B Test Analysis"):
                st.markdown("**Condition Comparison**")

                # Create condition analysis
                assignments = json_data['ab_test_assignments']
                condition_analysis = {}

                for persona_id, condition_id in assignments.items():
                    if condition_id not in condition_analysis:
                        condition_analysis[condition_id] = []

                    # Find responses for this persona
                    if 'persona_id' in filtered_data.columns:
                        persona_responses = filtered_data[
                            filtered_data['persona_id'] == persona_id
                        ]
                    else:
                        # Backward compatibility for historical name-keyed runs.
                        persona_responses = filtered_data[
                            filtered_data['persona_name'] == persona_id
                        ]
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
                            st.markdown("**Condition Comparison**")
                            col1, col2 = st.columns(2)

                            with col1:
                                best_condition = max(condition_stats, key=lambda x: float(x['Avg Length']))
                                st.success(f"**Longest Responses:** {best_condition['Condition']} ({best_condition['Avg Length']} chars avg)")

                            with col2:
                                shortest_condition = min(condition_stats, key=lambda x: float(x['Avg Length']))
                                st.info(f"**Shortest Responses:** {shortest_condition['Condition']} ({shortest_condition['Avg Length']} chars avg)")

        # Message Testing specific analysis
        elif json_data and json_data.get('simulation_type') == 'message_testing':
            with st.expander("Message Testing Analysis"):
                st.markdown("**Response Patterns**")

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
                st.markdown("**Sample Responses**")
                sample_responses = filtered_data.nlargest(5, 'response_length')
                for idx, row in sample_responses.iterrows():
                    st.markdown(f"**{row['persona_name']}** - {row['response_length']} chars")
                    st.write(f"**Q:** {row['question']}")
                    st.write(f"**A:** {row['response']}")
                    st.markdown("---")

# Tab 3: Instrument Scores
with tab3:

    # Check if this is a standardized instrument
    instrument_name = json_data.get('instrument_name') if json_data else None

    if instrument_name:
        st.info(f"Standardized Instrument Detected: **{instrument_name}**")

        # Try to calculate scores
        try:
            # Get responses in wide format for scoring
            if csv_data is not None and not csv_data.empty:
                scores_df = SurveyScorer.calculate_scores_for_personas(csv_data, instrument_name)

                if not scores_df.empty:
                    st.success(f"Calculated scores for {len(scores_df)} personas")

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

                    # Internal consistency: pivot to persona x item matrix in questionnaire order
                    q_order = [q for q in (json_data.get('questions') or [])]
                    wide = (csv_data.assign(_num=pd.to_numeric(csv_data['response'], errors='coerce'))
                            .pivot_table(index='persona_name', columns='question', values='_num', aggfunc='first'))
                    if q_order:
                        wide = wide.reindex(columns=[q for q in q_order if q in wide.columns])
                    wide = wide.dropna()
                    if wide.shape[0] >= 2 and wide.shape[1] >= 2:
                        alpha = cronbach_alpha(wide.values)
                        if not pd.isna(alpha):
                            st.metric("Cronbach's α", f"{alpha:.2f}",
                                      help="Internal consistency across items. ≥0.7 is the human-data benchmark; "
                                           "synthetic panels often score lower — treat as a validity signal.")

                    st.markdown("---")

                    # Score distribution
                    st.markdown("**Score Distribution by Severity**")
                    severity_counts = scores_df['severity'].value_counts()
                    st.bar_chart(severity_counts)

                    st.markdown("---")

                    # Individual scores table
                    st.markdown("**Individual Persona Scores**")
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
                        label="Download Scores CSV",
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
        st.info("This appears to be a custom survey (no standardized instrument detected).")
        st.write("Automated scoring is only available for standardized instruments like PHQ-9, GAD-7, PSS-10, and WHO-5.")
        st.write("You can still view all responses in the other tabs.")

# Tab 4: Detailed Responses
with tab4:

    if json_data:
        # Group responses by question or persona
        view_by = st.radio("View by:", ["Question", "Persona"], horizontal=True)

        if view_by == "Question":
            # Group by question
            for question in json_data['questions']:
                st.markdown(f"**Q: {question}**")

                question_responses = [r for r in json_data['responses'] if r['question'] == question]

                for response_data in question_responses:
                    with st.expander(f"**{response_data['persona_name']}** ({response_data.get('persona_occupation', '—')})"):
                        st.write(response_data['response'])

                        # Show conversation history if available (not nested)
                        if response_data.get('conversation_history'):
                            st.markdown("---")
                            st.markdown("**Conversation History:**")
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
                st.markdown(f"**{persona_name}**")
                st.caption(f"{first_response.get('persona_age', '—')} years old, {first_response.get('persona_occupation', '—')}")

                for response_data in persona_responses:
                    with st.expander(f"**Q:** {response_data['question']}"):
                        st.write(response_data['response'])

                st.markdown("---")

# Tab 5: Export
with tab5:

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**CSV Export**")
        st.write("Flat format suitable for spreadsheet analysis")

        if csv_data is not None:
            csv_string = csv_data.to_csv(index=False)

            st.download_button(
                label="Download CSV",
                data=csv_string,
                file_name=selected_result['csv_file'],
                mime="text/csv",
                use_container_width=True
            )

            st.info(f"File: {selected_result['csv_file']}\nSize: {len(csv_data)} rows")

            wide_export = results_to_wide(csv_data)
            st.download_button(
                label="Download Wide CSV",
                data=wide_export.to_csv(index=False),
                file_name=f"wide_{selected_result['csv_file']}",
                mime="text/csv",
                use_container_width=True,
                help="One persona per row with all population variables and one column per question",
            )

    with col2:
        st.markdown("**JSON Export**")
        st.write("Detailed format including conversation history")

        if json_data:
            json_string = json.dumps(json_data, indent=2)

            st.download_button(
                label="Download JSON",
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
            st.markdown("**Message Testing Export**")

            if 'intervention_text' in json_data:
                st.write("**Message/Intervention Text:**")
                st.text_area("Intervention Text", json_data.get('intervention_text'), height=100, disabled=True)

                # Export intervention text separately
                st.download_button(
                    label="Download Intervention Text",
                    data=json_data.get('intervention_text'),
                    file_name=f"intervention_{selected_result['csv_file'].replace('.csv', '.txt')}",
                    mime="text/plain",
                    use_container_width=True
                )

        elif json_data.get('simulation_type') == 'ab_testing':
            st.markdown("**A/B Testing Export**")

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
                    label="Download A/B Test Configuration",
                    data=json.dumps(ab_config, indent=2),
                    file_name=f"ab_test_config_{selected_result['csv_file'].replace('.csv', '.json')}",
                    mime="application/json",
                    use_container_width=True
                )

    # Text Analysis & Word Cloud - Available for ALL result types
    st.markdown("---")
    st.markdown("**Text Analysis & Word Cloud**")
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
            label="Download Raw Responses (TXT)",
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
            label="Download Responses (CSV)",
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
            if st.button("Generate Word Cloud", key="generate_wc"):
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
    st.markdown("**Delete This Result**")

    @st.dialog("Delete this result?")
    def confirm_delete_single():
        st.write(f"Permanently delete **{selected_result['name']}**? This cannot be undone.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Delete", type="primary", use_container_width=True, key="confirm_delete_btn"):
                if st.session_state.results_storage.delete_result(selected_result['name']):
                    st.toast(f"Deleted {selected_result['name']}")
                    st.rerun()
                else:
                    st.error("Failed to delete result")
        with c2:
            if st.button("Cancel", use_container_width=True, key="cancel_delete_btn"):
                st.rerun()

    if st.button("Delete this result", key="delete_single_btn"):
        confirm_delete_single()

# Footer
st.markdown("---")
st.caption("Tip: Export results to CSV for further analysis in spreadsheet software or statistical tools.")
