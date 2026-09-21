"""Introduction page for the synthetic-audience research application."""
import streamlit as st

from src import (
    PersonaManager, ResultsStorage, render_navigation, render_page_header,
    section, workflow_strip, feature_grid,
)
from src.styles import apply_global_styles

st.set_page_config(
    page_title="auto_sim_ai",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_global_styles()

# Navigation status remains useful on the introduction page.
st.session_state.setdefault('llm_client', None)
st.session_state.setdefault('selected_model', None)
st.session_state.setdefault('persona_manager', PersonaManager())
st.session_state.setdefault('results_storage', ResultsStorage())

render_navigation(current_page="home")
render_page_header(
    "Synthetic audience research in one workspace.",
    "Create a traceable population, run four kinds of AI-assisted studies, and inspect response quality before using the results.",
    eyebrow="auto_sim_ai",
)

primary, secondary, _space = st.columns([1.15, 1, 3.2])
with primary:
    if st.button("Set up workspace →", type="primary", use_container_width=True):
        st.switch_page("pages/1_Setup.py")
with secondary:
    if st.button("Explore simulation", use_container_width=True):
        st.switch_page("pages/2_Simulation.py")

workflow_strip([
    ("01", "Set up", "Connect a model and build the population."),
    ("02", "Simulate", "Configure a study and generate responses."),
    ("03", "Analyze", "Check validity, compare groups, and export."),
])

section("Study modes", first=True)
feature_grid([
    ("Survey", "Questionnaire simulation",
     "Run open-ended questions or structured scales across the selected population."),
    ("Message testing", "Reaction testing",
     "Show one message or intervention to each persona, then collect independent reactions."),
    ("A/B testing", "Condition comparison",
     "Assign weighted or stratified groups and compare numeric outcomes with corrected tests."),
    ("Longitudinal", "Multi-wave research",
     "Follow the same stable persona IDs over time with memory and optional interventions."),
])

section("What the application keeps visible")
feature_grid([
    ("Population", "Stable respondent identity",
     "Prompt-generated and CSV-imported personas retain demographics, custom fields, and unique IDs."),
    ("Execution", "Reproducible run context",
     "Saved results include model, seed, population, provider, validation state, and study configuration."),
    ("Quality", "Auditable synthetic evidence",
     "Invalid responses remain visible; answer collapse, subgroup patterns, and condition effects are reported."),
])

with st.container(border=True):
    c1, c2 = st.columns([2.5, 1])
    with c1:
        st.markdown("**Ready to begin?**")
        st.caption("Setup places model configuration and population construction together before simulation.")
    with c2:
        if st.button("Open Setup →", type="primary", use_container_width=True, key="home_bottom_setup"):
            st.switch_page("pages/1_Setup.py")

st.markdown(
    '<div class="home-footer">Synthetic responses are exploratory evidence and do not replace '
    'human participants or external validation.</div>',
    unsafe_allow_html=True,
)
