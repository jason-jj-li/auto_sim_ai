"""Reusable horizontal model-connection panel for the Setup workspace."""
import streamlit as st

from .llm_client import LMStudioClient


PROVIDERS = ["Local (LM Studio)", "DeepSeek", "OpenAI", "Custom OpenAI-Compatible"]


def _init_connection_state():
    defaults = {
        'llm_client': None,
        'base_url': 'http://127.0.0.1:1234/v1',
        'selected_model': None,
        'available_models': [],
        'connection_verified': False,
        'api_provider': 'Local (LM Studio)',
        'api_key': None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def render_model_connection():
    """Render provider, credentials, model, and connection action in one row."""
    _init_connection_state()
    current_provider = st.session_state.api_provider
    provider_index = PROVIDERS.index(current_provider) if current_provider in PROVIDERS else 0

    with st.container(border=True):
        provider_col, endpoint_col, model_col, action_col = st.columns(
            [1.05, 1.55, 1.25, 0.95], gap="medium"
        )

        with provider_col:
            provider = st.selectbox(
                "Provider", PROVIDERS, index=provider_index,
                key="setup_api_provider", help="Execution backend for every simulation mode",
            )
            if provider != st.session_state.api_provider:
                st.session_state.api_provider = provider
                st.session_state.llm_client = None
                st.session_state.available_models = []
                st.session_state.selected_model = None
                st.session_state.connection_verified = False
                st.session_state.setup_model_name = ""
                st.session_state.parallel_workers = 1 if provider == "Local (LM Studio)" else 5

        with endpoint_col:
            if provider == "Local (LM Studio)":
                new_url = st.text_input(
                    "API endpoint", value=st.session_state.base_url,
                    placeholder="http://127.0.0.1:1234/v1", key="setup_local_url",
                )
                api_key = None
            elif provider == "DeepSeek":
                new_url = "https://api.deepseek.com/v1"
                api_key = st.text_input(
                    "DeepSeek API key", type="password", placeholder="sk-…",
                    key="setup_deepseek_key",
                )
            elif provider == "OpenAI":
                new_url = "https://api.openai.com/v1"
                api_key = st.text_input(
                    "OpenAI API key", type="password", placeholder="sk-…",
                    key="setup_openai_key",
                )
            else:
                new_url = st.text_input(
                    "API endpoint", value=st.session_state.base_url,
                    placeholder="https://api.example.com/v1", key="setup_custom_url",
                )
                api_key = st.text_input(
                    "API key", type="password", placeholder="Optional",
                    key="setup_custom_key",
                )

        with model_col:
            manual_model = st.text_input(
                "Model", value=st.session_state.selected_model or "",
                placeholder="Auto-discover or enter exact name", key="setup_model_name",
                help="An exact model name overrides automatic selection",
            )
            if st.session_state.available_models:
                st.caption(f"{len(st.session_state.available_models)} model(s) discovered")

        if new_url != st.session_state.base_url:
            st.session_state.base_url = new_url
            st.session_state.llm_client = None
            st.session_state.connection_verified = False
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
            st.session_state.llm_client = None
            st.session_state.connection_verified = False

        cloud = provider != "Local (LM Studio)"
        st.session_state.setdefault('parallel_workers', 5 if cloud else 1)
        st.session_state.enable_parallel = cloud
        if not cloud:
            st.session_state.parallel_workers = 1

        with action_col:
            st.markdown('<div class="connection-action-label">Connection</div>', unsafe_allow_html=True)
            test_connection = st.button(
                "Test connection", type="primary", use_container_width=True,
                key="setup_test_connection",
            )
            if st.session_state.llm_client is not None:
                st.markdown('<span class="chip chip-ok">Connected</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="chip">Not connected</span>', unsafe_allow_html=True)

        if test_connection:
            if cloud and not api_key:
                st.error(f"API key is required for {provider}")
                return
            with st.spinner(f"Connecting to {provider}…"):
                try:
                    client = LMStudioClient(base_url=new_url, api_key=api_key or None)
                    success, message = client.test_connection()
                    if not success:
                        st.session_state.llm_client = None
                        st.session_state.connection_verified = False
                        st.error(f"Connection failed: {message}")
                        return

                    models = client.get_available_models() or []
                    selected = manual_model.strip() or (models[0] if models else None)
                    st.session_state.available_models = models
                    if selected:
                        st.session_state.selected_model = selected
                        st.session_state.llm_client = client
                        st.session_state.connection_verified = True
                        st.toast(f"Connected — {selected}")
                        st.rerun()
                    else:
                        st.session_state.llm_client = None
                        st.warning("Endpoint connected, but no model was discovered. Enter an exact model name and test again.")
                except Exception as exc:
                    st.session_state.llm_client = None
                    st.session_state.connection_verified = False
                    st.error(f"Connection failed: {exc}")

    if st.session_state.llm_client and st.session_state.selected_model:
        st.caption(
            f"Active: **{st.session_state.selected_model}** · "
            f"{st.session_state.api_provider} · {st.session_state.base_url}"
        )
    elif st.session_state.api_provider == "Local (LM Studio)":
        st.caption("LM Studio: load a model, start the local server, then test the connection here.")
