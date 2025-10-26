"""Main Streamlit application for LLM Simulation Survey System."""
import streamlit as st
from src import (
    LMStudioClient, PersonaManager, ResultsStorage,
    render_navigation, ConnectionManager, InputValidator, render_system_status_badge
)
from src.styles import apply_global_styles

# Page configuration
st.set_page_config(
    page_title="LLM Simulation Survey System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply global design system
apply_global_styles()

# Initialize session state
if 'llm_client' not in st.session_state:
    st.session_state.llm_client = None
if 'base_url' not in st.session_state:
    st.session_state.base_url = "http://127.0.0.1:1234"
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = None
if 'available_models' not in st.session_state:
    st.session_state.available_models = []
if 'persona_manager' not in st.session_state:
    st.session_state.persona_manager = PersonaManager()
if 'results_storage' not in st.session_state:
    st.session_state.results_storage = ResultsStorage()
if 'connection_verified' not in st.session_state:
    st.session_state.connection_verified = False
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True
if 'api_provider' not in st.session_state:
    st.session_state.api_provider = "Local (LM Studio)"
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

# Top Navigation
render_navigation(current_page="home")

# System Status Sidebar
render_system_status_badge()

# Hero Section
st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    color: white;
">
    <h1 style="color: white; font-size: 2.8rem; font-weight: 700; margin-bottom: 0.5rem;">
        🔬 LLM Simulation Survey System
    </h1>
    <p style="color: rgba(255,255,255,0.95); font-size: 1.2rem; line-height: 1.6; margin-bottom: 0;">
        Simulate surveys and interventions using AI-powered personas to understand how different 
        demographic groups respond to questions and messaging.
    </p>
</div>
""", unsafe_allow_html=True)

# First-time user onboarding (simplified, compact version)
if st.session_state.first_visit:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    ">
        <h3 style="color: white; margin-top: 0;">👋 Welcome! Get Started in 3 Steps</h3>
        <p style="color: rgba(255,255,255,0.95); margin-bottom: 0.5rem;">
            <strong>1)</strong> Connect to LLM below → 
            <strong>2)</strong> Add personas (Setup page) → 
            <strong>3)</strong> Run simulation (Simulate page)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_dismiss, col_detail = st.columns([1, 4])
    with col_dismiss:
        if st.button("✅ Got it", type="primary", use_container_width=True):
            st.session_state.first_visit = False
            st.rerun()
    with col_detail:
        with st.expander("📖 View detailed guide"):
            st.markdown("""
            ### Quick Start Guide
            
            **1️⃣ Connect to LLM** (below on this page)
            - Option A (FREE): Start LM Studio locally → Click "Test Connection"
            - Option B: Enter DeepSeek/OpenAI API key → Click "Test Connection"
            
            **2️⃣ Add Personas** (Setup page)
            - Create 5-10 diverse personas manually
            - Or upload a CSV file with persona data
            - Or generate synthetic population from distributions
            
            **3️⃣ Run Simulation** (Simulate page)
            - Choose survey or intervention mode
            - Select personas and questions
            - Click "Run Simulation" and watch real-time progress!
            
            **💡 Pro Tips:**
            - Use local LM Studio = $0 cost, complete privacy
            - Start with 5 personas for fast testing
            - Check Results page to export data as CSV/JSON
            """)

st.markdown("---")

# Connection status and quick stats in main area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div style="
        background: white;
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    ">
        <h3 style="color: #667eea; font-size: 1.3rem; margin-bottom: 1rem;">🔌 LLM Connection</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # API Provider Selection
    api_provider = st.selectbox(
        "API Provider",
        ["Local (LM Studio)", "DeepSeek", "OpenAI", "Custom OpenAI-Compatible"],
        help="Choose your LLM provider",
        key="api_provider_select"
    )
    
    # Initialize session state for api_provider and api_key if not exists
    if 'api_provider' not in st.session_state:
        st.session_state.api_provider = "Local (LM Studio)"
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None
    if 'enable_parallel' not in st.session_state:
        st.session_state.enable_parallel = False
    if 'parallel_workers' not in st.session_state:
        st.session_state.parallel_workers = 5
    
    # Store provider in session state
    if st.session_state.api_provider != api_provider:
        st.session_state.api_provider = api_provider
        st.session_state.llm_client = None  # Reset client
        st.session_state.available_models = []
        st.session_state.selected_model = None
        # Auto-enable parallel for cloud APIs
        if api_provider in ["DeepSeek", "OpenAI", "Custom OpenAI-Compatible"]:
            st.session_state.enable_parallel = True
        else:
            st.session_state.enable_parallel = False
    
    # Configure based on provider
    if api_provider == "Local (LM Studio)":
        # API URL input
        new_url = st.text_input(
            "LM Studio API URL",
            value=st.session_state.base_url,
            placeholder="http://localhost:1234/v1",
            help="Default: http://127.0.0.1:1234/v1",
            key="home_url_input"
        )
        
        api_key = None  # No API key needed for local
        
    elif api_provider == "DeepSeek":
        st.info("💡 DeepSeek offers affordable API access. Get your API key at: https://platform.deepseek.com")
        
        new_url = "https://api.deepseek.com/v1"
        st.text_input(
            "API URL",
            value=new_url,
            disabled=True,
            help="DeepSeek API endpoint"
        )
        
        api_key = st.text_input(
            "DeepSeek API Key *",
            type="password",
            placeholder="sk-...",
            help="Your DeepSeek API key from platform.deepseek.com",
            key="deepseek_api_key"
        )
        
    elif api_provider == "OpenAI":
        st.info("💡 Using OpenAI API. Get your API key at: https://platform.openai.com/api-keys")
        
        new_url = "https://api.openai.com/v1"
        st.text_input(
            "API URL",
            value=new_url,
            disabled=True,
            help="OpenAI API endpoint"
        )
        
        api_key = st.text_input(
            "OpenAI API Key *",
            type="password",
            placeholder="sk-...",
            help="Your OpenAI API key",
            key="openai_api_key"
        )
        
    else:  # Custom OpenAI-Compatible
        new_url = st.text_input(
            "API URL",
            value="https://api.example.com/v1",
            placeholder="https://api.example.com/v1",
            help="Enter the base URL for your OpenAI-compatible API (including /v1)",
            key="custom_url_input"
        )
        
        api_key = st.text_input(
            "API Key (if required)",
            type="password",
            placeholder="your-api-key",
            help="API key if your provider requires authentication",
            key="custom_api_key"
        )

    if new_url != st.session_state.base_url:
        st.session_state.base_url = new_url
        st.session_state.llm_client = None  # Reset client
        st.session_state.available_models = []
        st.session_state.selected_model = None
    
    # Store API key in session state
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        st.session_state.llm_client = None  # Reset client
    
    # Initialize parallel settings (will be configured in simulation page)
    if api_provider in ["DeepSeek", "OpenAI", "Custom OpenAI-Compatible"]:
        if 'enable_parallel' not in st.session_state:
            st.session_state.enable_parallel = False
        if 'parallel_workers' not in st.session_state:
            st.session_state.parallel_workers = 5
    else:
        # Local LM Studio - no parallel support
        st.session_state.enable_parallel = False
        st.session_state.parallel_workers = 1
    
    # Optional: Manual model name input
    st.markdown("**Or specify model name directly:**")
    
    # Provide suggestions based on provider
    if api_provider == "DeepSeek":
        placeholder = "deepseek-chat"
        st.info("💡 **Recommended**: Use `deepseek-chat` for general tasks or `deepseek-coder` for coding tasks")
    elif api_provider == "OpenAI":
        placeholder = "e.g., gpt-4, gpt-3.5-turbo, gpt-4o"
    else:
        placeholder = "e.g., llama-2-7b-chat, mistral-7b-instruct"
    
    manual_model = st.text_input(
        "Model Name (optional)",
        value="",
        placeholder=placeholder,
        help="Leave empty to discover models automatically, or enter the exact model name",
        key="manual_model_input"
    )
    
    if manual_model:
        st.session_state.selected_model = manual_model
        st.info(f"📝 Manual model set: {manual_model}")

    # Single Test Connection button
    if st.button("🔍 Test Connection", type="primary", use_container_width=True):
        # Validate API key for online providers
        if api_provider != "Local (LM Studio)" and not api_key:
            st.error(f"❌ API key is required for {api_provider}")
            st.stop()
        
        spinner_msg = f"Testing connection to {api_provider}..."
        with st.spinner(spinner_msg):
            try:
                temp_client = LMStudioClient(
                    base_url=st.session_state.base_url,
                    api_key=api_key if api_key else None
                )
                success, message = temp_client.test_connection()
                
                if success:
                    # Get models
                    models = temp_client.get_available_models()
                    
                    if models:
                        st.session_state.available_models = models
                        
                        # Auto-select model (manual entry takes priority)
                        if manual_model:
                            st.session_state.selected_model = manual_model
                            model_to_use = manual_model
                        else:
                            # Use first discovered model
                            st.session_state.selected_model = models[0]
                            model_to_use = models[0]
                        
                        # Set up client
                        st.session_state.llm_client = temp_client
                        st.session_state.connection_verified = True  # Mark as verified
                        
                        # Show success
                        st.success("✅ System Ready!")
                        provider_name = api_provider if api_provider else "LLM API"
                        st.info(f"""
                        **Connection Status:**
                        - 🟢 Provider: {provider_name}
                        - 🟢 API: Connected
                        - 🟢 Models Found: {len(models)}
                        - 🟢 Active Model: {model_to_use}
                        
                        **You're all set!** Go to the Setup page to add personas, then Simulate!
                        """)
                        
                        # Show all available models
                        with st.expander("View All Available Models"):
                            for i, model in enumerate(models, 1):
                                is_active = "✓" if model == model_to_use else " "
                                st.write(f"{i}. [{is_active}] {model}")
                        
                    else:
                        st.warning("⚠️ Connected but no models found")
                        if api_provider == "Local (LM Studio)":
                            st.info("""
                            **Next Steps:**
                            1. Go to LM Studio
                            2. Load a model from the model library
                            3. Come back and test connection again
                            """)
                        else:
                            st.info("""
                            **Next Steps:**
                            1. Make sure you have access to models through your API key
                            2. Enter the model name manually above
                            3. Test connection again
                            """)
                        st.session_state.available_models = []
                        st.session_state.llm_client = None
                else:
                    st.error(f"❌ Connection failed: {message}")
                    st.session_state.llm_client = None
                    
            except Exception as e:
                error_msg = str(e)
                st.error(f"❌ Connection failed: {error_msg}")
                st.session_state.llm_client = None
                
                # Provide specific troubleshooting based on error
                if "502" in error_msg or "Bad Gateway" in error_msg:
                    st.warning("""
                    **🔴 502 Error - LM Studio Server Not Running**
                    
                    **Fix:**
                    1. ✅ Open LM Studio application
                    2. ✅ Click the **"Local Server"** tab (↔️ icon on left)
                    3. ✅ Click **"Start Server"** button
                    4. ✅ Wait for "Server running on http://localhost:1234"
                    5. ✅ Make sure a model is loaded
                    6. ✅ Test connection again
                    """)
                elif "Connection refused" in error_msg or "Failed to connect" in error_msg:
                    st.warning("""
                    **Connection Refused**
                    
                    **Fix:**
                    1. ✅ Is LM Studio running?
                    2. ✅ Is the server started in "Local Server" tab?
                    3. ✅ Using the right port? (default: 1234)
                    """)
                elif "timeout" in error_msg.lower():
                    st.warning("""
                    **Connection Timeout**
                    
                    **Fix:**
                    1. ✅ Wait for LM Studio to fully start
                    2. ✅ Check firewall settings
                    3. ✅ Verify the URL is correct
                    """)
                else:
                    st.info("""
                    **Troubleshooting Steps:**
                    
                    1. Open LM Studio application
                    2. Load a model from the library
                    3. Go to "Local Server" tab
                    4. Click "Start Server"
                    5. Wait for server to fully start
                    6. Test connection again
                    """)
    
    st.markdown("---")
    
    # Display connection status
    if st.session_state.llm_client and st.session_state.selected_model:
        st.success(f"✅ System Ready - Connected to LM Studio")
        st.info(f"**Active Model:** {st.session_state.selected_model}")
        st.caption(f"**API URL:** {st.session_state.base_url}")
    else:
        st.warning("⚠️ Not connected to LM Studio")
        st.info("👆 Click 'Test Connection' to verify your setup and connect")
    
    # Quick setup guide
    with st.expander("📖 How to Start LM Studio Server", expanded=False):
        st.markdown("""
        ### Step-by-Step Guide:
        
        1. **Open LM Studio** application on your computer
        
        2. **Load a Model** (if not already loaded):
           - Click the 🔍 **Search** icon on the left
           - Download a model (e.g., Llama 2 7B, Mistral 7B)
           - Click on the model to load it
        
        3. **Start the Server**:
           - Click the **↔️ Local Server** tab on the left sidebar
           - Click the **"Start Server"** button
           - Wait for the message: `Server running on http://localhost:1234`
        
        4. **Return here** and click **"🔄 Discover Models"**
        
        ### Verification:
        - ✅ LM Studio window is open
        - ✅ A model is loaded (shown in the top bar)
        - ✅ Server tab shows "Server running"
        - ✅ Port number is 1234 (or update URL above if different)
        
        ### Common Issues:
        - **502 Error**: Server not started → Click "Start Server" in LM Studio
        - **Connection Refused**: LM Studio not running → Open LM Studio
        - **No Models**: Load a model first → Go to Search tab in LM Studio
        """)

with col2:
    st.subheader("📊 Quick Stats")
    
    personas = st.session_state.persona_manager.load_all_personas()
    results = st.session_state.results_storage.list_results()
    
    st.metric("Total Personas", len(personas))
    st.metric("Total Simulations", len(results))
    
    st.markdown("---")
    st.markdown("""
    **Need Help?**
    
    1. Ensure LM Studio is running
    2. Load a model in LM Studio
    3. Check the API port (default: 1234)
    4. Test connection above
    """)

