"""Global UI styles for the editorial research workspace."""

GLOBAL_STYLES = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

    :root {
        --accent: #c4502f;
        --accent-hover: #a63e21;
        --accent-light: #fae9e2;
        --bg: #f7f5f0;
        --surface: #ffffff;
        --surface-muted: #f1eee7;
        --border: #dedad0;
        --border-strong: #c9c3b7;
        --text: #18201c;
        --text-secondary: #696d67;
        --success: #286249;
        --success-bg: #e8f2ec;
        --warning: #9a6a1a;
        --error: #b3341f;
        --error-bg: #fbe9e5;
        --radius-sm: 6px;
        --radius: 10px;
        --radius-lg: 16px;
        --serif: 'Fraunces', Georgia, serif;
        --sans: 'IBM Plex Sans', -apple-system, sans-serif;
        --mono: 'IBM Plex Mono', monospace;
    }

    html { scroll-behavior: smooth; }
    .stApp { background: var(--bg); font-family: var(--sans); color: var(--text); }
    .block-container { padding-top: 1.25rem; padding-bottom: 4rem; max-width: 1240px; }

    /* Sidebar hidden — top nav is the navigation; header chrome hidden too */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], [data-testid="stHeader"] { display: none !important; }

    /* Typography — serif display, small-caps kickers (!important beats Streamlit theme font) */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3 {
        font-family: var(--serif) !important; color: var(--text); letter-spacing: -0.01em;
    }
    h1 { font-size: clamp(2rem, 4vw, 3.15rem) !important; font-weight: 600; line-height: 1.08 !important; }
    h2 { font-size: 1.45rem !important; font-weight: 600; }
    h3 { font-size: 1.15rem !important; font-weight: 600; }
    p, .stMarkdown, label, .stCaption { font-family: var(--sans); }
    p, .stMarkdown { line-height: 1.6; color: var(--text); }
    .stCaption, small { color: var(--text-secondary); font-size: 0.82rem; }
    a { color: var(--accent); }
    ::selection { background: var(--accent-light); }

    .kicker {
        font-family: var(--sans); font-size: 0.72rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.14em; color: var(--accent);
        margin-bottom: 0.2rem;
    }
    .page-header { max-width: 790px; padding: 2.4rem 0 1.65rem; }
    .page-header h1 { margin: 0.25rem 0 0.65rem; }
    .page-subtitle { color: var(--text-secondary) !important; font-size: 1.04rem; line-height: 1.65; margin: 0; max-width: 720px; }
    .hero-actions { margin: -0.5rem 0 1.7rem; }

    /* Wordmark in nav bar */
    .wordmark {
        font-family: var(--mono); font-size: 0.88rem; font-weight: 500;
        color: var(--text); letter-spacing: -0.02em; padding-top: 0.45rem;
    }
    .wordmark::before { content: '●'; color: var(--accent); margin-right: 0.55rem; font-size: 0.7rem; }
    .nav-status { text-align: right; padding-top: 0.42rem; }
    .nav-rule { border-bottom: 1px solid var(--border); padding-top: 0.55rem; }
    div[data-testid="stHorizontalBlock"]:has(.wordmark) {
        position: sticky; top: 0; z-index: 999; background: rgba(247,245,240,0.96);
        padding: 0.55rem 0 0.45rem; backdrop-filter: blur(12px);
    }

    /* Section header — the ONE section anatomy: serif title over a hairline */
    .section-head {
        font-family: var(--serif); font-size: 1.15rem; font-weight: 600; color: var(--text);
        border-bottom: 1px solid var(--border); padding-bottom: 0.35rem;
        margin: 1.5rem 0 0.9rem; letter-spacing: -0.01em;
    }
    .section-head-first { margin-top: 0.2rem; }

    /* Bordered panel (st.container(border=True)) — paper surface, hairline frame */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: var(--radius-lg); padding: 0.25rem;
    }

    /* Buttons — secondary = ghost link, primary = solid accent */
    .stButton button {
        font-family: var(--sans); font-weight: 500; font-size: 0.9rem;
        border-radius: var(--radius-sm); box-shadow: none; white-space: nowrap;
        border: 1px solid transparent; background: transparent; color: var(--text-secondary);
        transition: color 0.15s ease, background 0.15s ease, border-color 0.15s ease;
    }
    .stButton button:hover { color: var(--accent); background: var(--accent-light); }
    .stButton button[kind="primary"] {
        background: var(--accent); border-color: var(--accent); color: #fff;
    }
    .stButton button[kind="primary"]:hover { background: var(--accent-hover); color: #fff; }
    .stButton button:disabled { opacity: 0.4; }
    .stButton button:focus-visible, .stDownloadButton button:focus-visible {
        outline: 3px solid rgba(196,80,47,0.25); outline-offset: 2px;
    }
    /* Form submit + download buttons keep an outlined look */
    .stFormSubmitButton button, .stDownloadButton button {
        border: 1px solid var(--border); background: var(--surface); color: var(--text);
    }
    .stFormSubmitButton button:hover, .stDownloadButton button:hover {
        border-color: var(--accent); color: var(--accent); background: var(--surface);
    }

    /* Stat cards — serif numerals, hairline frame */
    .ui-card {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: var(--radius); padding: 1rem 1.15rem; min-height: 92px;
        transition: transform 0.16s ease, border-color 0.16s ease;
    }
    .ui-card:hover { transform: translateY(-1px); border-color: var(--border-strong); }
    .ui-card .ui-card-label {
        font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.12em; color: var(--text-secondary); margin-bottom: 0.2rem;
    }
    .ui-card .ui-card-value { font-family: var(--serif) !important; font-size: 1.7rem; font-weight: 600; color: var(--text); }

    /* Readiness / nav chips */
    .chip {
        display: inline-block; padding: 0.18rem 0.65rem; margin-right: 0.4rem;
        border-radius: 9999px; font-size: 0.78rem; font-weight: 500;
        border: 1px solid var(--border); color: var(--text-secondary); background: var(--surface);
    }
    .chip-ok { color: var(--success); border-color: #bfdccd; background: var(--success-bg); }
    .chip-bad { color: var(--error); border-color: #ecc5bc; background: var(--error-bg); }

    /* Tabs — small caps, accent underline */
    .stTabs [data-baseweb="tab-list"] { gap: 1.4rem; border-bottom: 1px solid var(--border); }
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary); font-weight: 500; font-size: 0.85rem;
        text-transform: uppercase; letter-spacing: 0.06em;
    }
    .stTabs [aria-selected="true"] { color: var(--accent); background: transparent; }
    .stTabs [data-baseweb="tab-highlight"] { background: var(--accent); }

    /* Workflow strip + simulation stepper */
    .workflow-strip {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px;
        background: var(--border); border: 1px solid var(--border);
        border-radius: var(--radius-lg); overflow: hidden; margin: 0 0 2rem;
    }
    .workflow-item { display: flex; gap: 0.9rem; padding: 1rem 1.15rem; background: var(--surface); }
    .workflow-item strong { font-size: 0.88rem; color: var(--text); }
    .workflow-item p { font-size: 0.78rem; color: var(--text-secondary); margin: 0.15rem 0 0; line-height: 1.4; }
    .workflow-number { font-family: var(--mono); color: var(--accent); font-size: 0.72rem; padding-top: 0.18rem; }
    .feature-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 0.8rem; margin: 0 0 1.7rem;
    }
    .feature-card {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: var(--radius); padding: 1.15rem 1.2rem 1.25rem;
        min-height: 164px; transition: transform 0.16s ease, border-color 0.16s ease;
    }
    .feature-card:hover { transform: translateY(-2px); border-color: var(--border-strong); }
    .feature-card h3 { font-size: 1.02rem !important; margin: 0.45rem 0 0.4rem; }
    .feature-card p { color: var(--text-secondary); font-size: 0.84rem; line-height: 1.55; margin: 0; }
    .feature-kicker { font-family: var(--mono); color: var(--accent); font-size: 0.68rem; letter-spacing: 0.06em; text-transform: uppercase; }
    .connection-intro { max-width: 700px; color: var(--text-secondary); margin: -0.35rem 0 1.1rem; font-size: 0.9rem; }
    .connection-action-label { font-size: 0.86rem; font-weight: 500; margin: 0 0 0.42rem; color: var(--text); }
    .home-footer { margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid var(--border); color: var(--text-secondary); font-size: 0.76rem; }
    .stepper { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1rem 1.15rem; margin-bottom: 1.35rem; }
    .step-list { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; }
    .step-item { display: flex; align-items: center; gap: 0.55rem; color: var(--text-secondary); position: relative; }
    .step-item:not(:last-child)::after { content: ''; position: absolute; left: 2rem; right: 0.5rem; top: 0.85rem; height: 1px; background: var(--border); }
    .step-marker { position: relative; z-index: 1; display: grid; place-items: center; width: 1.7rem; height: 1.7rem; flex: 0 0 1.7rem; border: 1px solid var(--border); border-radius: 50%; background: var(--surface); font-family: var(--mono); font-size: 0.68rem; }
    .step-label { position: relative; z-index: 1; background: var(--surface); padding-right: 0.5rem; font-size: 0.8rem; font-weight: 500; }
    .step-done .step-marker { background: var(--success-bg); border-color: #b7d6c6; color: var(--success); }
    .step-active { color: var(--text); }
    .step-active .step-marker { background: var(--accent); color: #fff; border-color: var(--accent); }
    .step-context { border-top: 1px solid var(--border); margin-top: 0.85rem; padding-top: 0.7rem; color: var(--text-secondary); font-size: 0.78rem; }

    .empty-state { text-align: center; padding: 2.7rem 1.5rem; border: 1px dashed var(--border-strong); border-radius: var(--radius-lg); background: rgba(255,255,255,0.55); }
    .empty-icon { color: var(--accent); font-size: 1.5rem; margin-bottom: 0.55rem; }
    .empty-title { font-family: var(--serif); color: var(--text); font-size: 1.1rem; font-weight: 600; }
    .empty-copy { color: var(--text-secondary); font-size: 0.86rem; max-width: 520px; margin: 0.35rem auto 0; }

    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input {
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        background: var(--surface) !important;
        font-family: var(--sans) !important;
        box-shadow: none !important;
    }
    [data-baseweb="select"] > div, [data-baseweb="input"] > div,
    [data-testid="stFileUploaderDropzone"] {
        border-color: var(--border) !important; border-radius: var(--radius-sm) !important;
        background: var(--surface) !important; box-shadow: none !important;
    }
    [data-testid="stFileUploaderDropzone"] { padding: 1.25rem; }
    [data-testid="stSegmentedControl"] { background: var(--surface-muted); border-radius: var(--radius); padding: 0.25rem; }
    [data-testid="stSegmentedControl"] button { border-radius: var(--radius-sm); }
    [data-testid="stDialog"] > div { border-radius: var(--radius-lg); border: 1px solid var(--border); }
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus, .stNumberInput input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px var(--accent-light) !important;
    }

    /* Expanders, dataframes, alerts: hairline + paper surfaces */
    .streamlit-expanderHeader, details {
        border-radius: var(--radius); border: 1px solid var(--border);
        background: var(--surface); font-weight: 500;
    }
    .stDataFrame { border-radius: var(--radius); overflow: hidden; border: 1px solid var(--border); }
    .stAlert { border-radius: var(--radius); font-family: var(--sans); }
    [data-testid="stToast"] { border: 1px solid var(--border); border-radius: var(--radius); }

    /* Metrics — serif numerals */
    [data-testid="stMetricValue"] { font-family: var(--serif) !important; font-size: 1.6rem; font-weight: 600; color: var(--text); }
    [data-testid="stMetricLabel"] { font-size: 0.72rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.1em; }

    /* Progress + code */
    [data-testid="stProgressBar"] > div > div { background: var(--accent); }
    code, .stCode, pre { font-family: var(--mono) !important; font-size: 0.82rem; }

    hr { border-color: var(--border); }

    @media (max-width: 768px) {
        h1 { font-size: 1.5rem; }
        .block-container { padding: 0.65rem 1rem 2.5rem; }
        .page-header { padding: 1.55rem 0 1rem; }
        .nav-status { display: none; }
        .workflow-strip { grid-template-columns: 1fr; }
        .feature-grid { grid-template-columns: 1fr; }
        .step-label { display: none; }
        .step-list { gap: 0.4rem; }
        .step-item:not(:last-child)::after { left: 1.8rem; right: 0; }
        .ui-card { min-height: 78px; padding: 0.8rem; }
        [data-testid="stMetricValue"] { font-size: 1.25rem; }
    }

    @media (prefers-reduced-motion: reduce) {
        html { scroll-behavior: auto; }
        *, *::before, *::after { transition: none !important; animation: none !important; }
    }
</style>
"""


def apply_global_styles():
    """Apply the design system to the current page. Call once at page top."""
    import streamlit as st
    st.markdown(GLOBAL_STYLES, unsafe_allow_html=True)
