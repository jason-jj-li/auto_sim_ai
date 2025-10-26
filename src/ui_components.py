"""Shared UI components for Streamlit pages."""
import streamlit as st


def render_navigation(current_page: str = "home"):
    """
    Render the top navigation bar with all page buttons.
    
    Args:
        current_page: Current page identifier ('home', 'setup', 'simulation', 'results')
    """
    # Modern navigation styling (simplified, flat design)
    st.markdown("""
    <style>
        /* Modern Navigation Bar */
        .nav-container {
            background: #ffffff;
            border-bottom: 1px solid #e2e8f0;
            padding: 0.75rem 0;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3, col4 = st.columns(4)
    
    # Check connection status
    is_connected = st.session_state.get('llm_client') is not None
    
    # Get persona count (including disk, session, and generated personas)
    from src import PersonaManager
    persona_manager = st.session_state.get('persona_manager', PersonaManager())
    disk_personas = persona_manager.load_all_personas()
    session_personas = st.session_state.get('session_personas', [])
    generated_personas = st.session_state.get('generated_personas', [])
    persona_count = len(disk_personas) + len(session_personas) + len(generated_personas)
    
    with col1:
        if st.button(
            "🏠 Home",
            use_container_width=True,
            type="primary" if current_page == "home" else "secondary"
        ):
            st.switch_page("app.py")
    
    with col2:
        # Show persona count badge
        setup_label = f"📋 Setup ({persona_count})" if persona_count > 0 else "📋 Setup ⚠️"
        if st.button(
            setup_label,
            use_container_width=True,
            type="primary" if current_page == "setup" else "secondary",
            help=f"{persona_count} personas loaded. Add more here."
        ):
            st.switch_page("pages/1_Setup.py")
    
    with col3:
        # Disable if not connected or no personas
        simulate_disabled = not is_connected or persona_count == 0
        simulate_help = "Quick persona-based surveys and message/intervention testing"
        if not is_connected:
            simulate_help = "⚠️ Connect to LLM first (Home page)"
        elif persona_count == 0:
            simulate_help = "⚠️ Add personas first (Setup page)"
            
        if st.button(
            "🎯 Simulate",
            use_container_width=True,
            type="primary" if current_page == "simulation" else "secondary",
            help=simulate_help,
            disabled=simulate_disabled
        ):
            st.switch_page("pages/2_Simulation.py")
    
    with col4:
        if st.button(
            "📊 Results",
            use_container_width=True,
            type="primary" if current_page == "results" else "secondary",
            help="View and analyze simulation results"
        ):
            st.switch_page("pages/3_Results.py")
    
    # Compact status bar below navigation
    st.markdown("---")
    
    # Status information in compact format
    status_col1, status_col2, status_col3 = st.columns([2, 1, 1])
    
    with status_col1:
        # Connection status
        if is_connected:
            model_name = st.session_state.get('selected_model', 'Unknown')
            provider = st.session_state.get('api_provider', 'Local (LM Studio)')
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: #16a34a;">
                <span>✅</span>
                <span><b>Connected:</b> {model_name}</span>
                <span style="color: #64748b;">({provider})</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: #dc2626;">
                <span>🔴</span>
                <span><b>Not Connected</b> - Go to Home to connect</span>
            </div>
            """, unsafe_allow_html=True)
    
    with status_col2:
        # Persona count
        st.markdown(f"""
        <div style="font-size: 0.875rem; color: #64748b;">
            👥 <b>{persona_count}</b> personas
        </div>
        """, unsafe_allow_html=True)
    
    with status_col3:
        # Results count
        from src import ResultsStorage
        results_storage = st.session_state.get('results_storage', ResultsStorage())
        results = results_storage.list_results()
        st.markdown(f"""
        <div style="font-size: 0.875rem; color: #64748b;">
            📊 <b>{len(results)}</b> simulations
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")


def render_system_status_badge():
    """Show system status in compact format (no sidebar)."""
    # Sidebar is now hidden - status is shown in navigation area or page content
    # This function is kept for backward compatibility but does nothing
    pass


def render_connection_status():
    """Render connection status banner."""
    if st.session_state.get('llm_client') and st.session_state.get('selected_model'):
        st.success(f"✅ Connected to LLM | Model: {st.session_state.selected_model}")
    else:
        st.warning("⚠️ Not connected to LLM - Go to Home page to connect")
        st.info("👉 Click '🏠 Home' to configure your LLM connection")


def render_page_header(title: str, icon: str = ""):
    """
    Render a consistent page header.
    
    Args:
        title: Page title
        icon: Optional emoji icon
    """
    if icon:
        st.title(f"{icon} {title}")
    else:
        st.title(title)

