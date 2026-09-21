"""Shared UI components for the Streamlit product shell."""
from html import escape
import streamlit as st


@st.cache_data(ttl=10)
def _disk_persona_count() -> int:
    """Disk persona count, cached so nav doesn't hit disk on every render."""
    from src import PersonaManager
    return len(PersonaManager().load_all_personas())


@st.cache_data(ttl=10)
def _results_count() -> int:
    from src import ResultsStorage
    return len(ResultsStorage().list_results())


def _persona_total() -> int:
    return (_disk_persona_count()
            + len(st.session_state.get('session_personas', []))
            + len(st.session_state.get('generated_personas', [])))


def render_navigation(current_page: str = "home"):
    """Single-row shell: wordmark + nav links + status chips, then one hairline."""
    pages = [
        ("home", "Home", "app.py"),
        ("setup", "Setup", "pages/1_Setup.py"),
        ("simulation", "Simulate", "pages/2_Simulation.py"),
        ("results", "Results", "pages/3_Results.py"),
    ]
    cols = st.columns([1.7, 0.68, 0.68, 0.85, 0.78, 3.6])
    with cols[0]:
        st.markdown('<div class="wordmark">auto_sim_ai</div>', unsafe_allow_html=True)
    for col, (key, label, path) in zip(cols[1:5], pages):
        with col:
            if st.button(label, use_container_width=True,
                         type="primary" if current_page == key else "secondary"):
                st.switch_page(path)

    connected = st.session_state.get('llm_client') is not None
    model = st.session_state.get('selected_model', '')
    conn_chip = (f'<span class="chip chip-ok">Model: {escape(str(model))}</span>' if connected
                 else '<span class="chip chip-bad">No model — connect on Home</span>')
    with cols[5]:
        st.markdown(
            f'<div class="nav-status">{conn_chip}'
            f'<span class="chip">{_persona_total()} personas</span>'
            f'<span class="chip">{_results_count()} results</span></div>',
            unsafe_allow_html=True)
    st.markdown('<div class="nav-rule"></div>', unsafe_allow_html=True)


def render_page_header(title: str, caption: str = "", eyebrow: str = "Research workspace"):
    """Consistent product-page header with a compact editorial hierarchy."""
    subtitle = f'<p class="page-subtitle">{escape(caption)}</p>' if caption else ''
    st.markdown(
        f'<header class="page-header"><div class="kicker">{escape(eyebrow)}</div>'
        f'<h1>{escape(title)}</h1>{subtitle}</header>',
        unsafe_allow_html=True,
    )


def section(title: str, first: bool = False):
    """Section header — serif title over a hairline. The one section anatomy."""
    cls = "section-head section-head-first" if first else "section-head"
    st.markdown(f'<div class="{cls}">{escape(str(title))}</div>', unsafe_allow_html=True)


def stat_cards(pairs):
    """One row of minimal stat cards. pairs: list of (label, value)."""
    if not pairs:
        return
    cols = st.columns(len(pairs))
    for col, (label, value) in zip(cols, pairs):
        with col:
            st.markdown(
                f'<div class="ui-card"><div class="ui-card-label">{escape(str(label))}</div>'
                f'<div class="ui-card-value">{escape(str(value))}</div></div>',
                unsafe_allow_html=True)


def render_stepper(current: int, steps, context: str = ""):
    """Render a responsive, accessible workflow stepper."""
    items = []
    for index, label in enumerate(steps, 1):
        state = "done" if index < current else "active" if index == current else "upcoming"
        marker = "✓" if state == "done" else str(index)
        current_attr = ' aria-current="step"' if state == "active" else ''
        items.append(
            f'<div class="step-item step-{state}"{current_attr}>'
            f'<span class="step-marker">{marker}</span>'
            f'<span class="step-label">{escape(str(label))}</span></div>'
        )
    context_html = f'<div class="step-context">{escape(context)}</div>' if context else ''
    st.markdown(
        f'<div class="stepper" role="navigation" aria-label="Simulation progress">'
        f'<div class="step-list">{"".join(items)}</div>{context_html}</div>',
        unsafe_allow_html=True,
    )


def render_empty_state(title: str, description: str, icon: str = "◇"):
    """Render a calm empty state; actions can be placed immediately after it."""
    st.markdown(
        f'<div class="empty-state"><div class="empty-icon">{escape(icon)}</div>'
        f'<div class="empty-title">{escape(title)}</div>'
        f'<div class="empty-copy">{escape(description)}</div></div>',
        unsafe_allow_html=True,
    )


def workflow_strip(items):
    """Compact three/four-part orientation strip used on landing pages."""
    blocks = []
    for number, title, description in items:
        blocks.append(
            f'<div class="workflow-item"><span class="workflow-number">{escape(str(number))}</span>'
            f'<div><strong>{escape(str(title))}</strong><p>{escape(str(description))}</p></div></div>'
        )
    st.markdown(f'<div class="workflow-strip">{"".join(blocks)}</div>', unsafe_allow_html=True)


def feature_grid(cards):
    """Render a responsive grid of product capabilities.

    Each card is ``(eyebrow, title, description)``. Content is escaped so the
    component is safe to reuse with dynamic labels later.
    """
    blocks = []
    for eyebrow, title, description in cards:
        blocks.append(
            '<article class="feature-card">'
            f'<div class="feature-kicker">{escape(str(eyebrow))}</div>'
            f'<h3>{escape(str(title))}</h3>'
            f'<p>{escape(str(description))}</p>'
            '</article>'
        )
    st.markdown(f'<div class="feature-grid">{"".join(blocks)}</div>', unsafe_allow_html=True)
