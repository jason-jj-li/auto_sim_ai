"""Setup page for persona and configuration management."""
import streamlit as st
import json
from src import Persona, PersonaManager, LMStudioClient, render_navigation, render_connection_status, PersonaGenerator, DistributionConfig, render_system_status_badge
from src.styles import apply_global_styles

st.set_page_config(page_title="Setup - LLM Simulation", page_icon="📋", layout="wide", initial_sidebar_state="collapsed")

# Apply global design system
apply_global_styles()

# Top Navigation
render_navigation(current_page="setup")

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
        📋 Setup & Configuration
    </h1>
    <p style="color: rgba(255,255,255,0.95); font-size: 1.1rem; line-height: 1.6; margin-bottom: 0;">
        Create and manage AI personas, configure survey settings, and prepare your simulation environment.
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize session state if needed
if 'persona_manager' not in st.session_state:
    st.session_state.persona_manager = PersonaManager()
if 'llm_client' not in st.session_state:
    st.session_state.llm_client = None
if 'base_url' not in st.session_state:
    st.session_state.base_url = "http://localhost:1234/v1"

# Initialize session-only personas (uploaded personas, cleared on browser close)
if 'session_personas' not in st.session_state:
    st.session_state.session_personas = []  # Temporary personas from CSV upload

# Connection Status Banner
render_connection_status()
st.markdown("---")

# Quick Status Summary at top
disk_personas = st.session_state.persona_manager.load_all_personas()
session_personas = st.session_state.get('session_personas', [])
generated_personas = st.session_state.get('generated_personas', [])
total_personas = len(disk_personas) + len(session_personas) + len(generated_personas)

if total_personas > 0:
    # Status Cards
    col1, col2, col3, col4 = st.columns(4)
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
                {total_personas}
            </div>
            <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
                Total Personas
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
                {len(disk_personas)}
            </div>
            <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
                � Saved
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
                {len(session_personas)}
            </div>
            <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
                📤 Uploaded
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
                {len(generated_personas)}
            </div>
            <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
                🎲 Generated
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_quick1, col_quick2, col_quick3 = st.columns([2, 2, 1])
    with col_quick1:
        if st.button("🚀 Go to Simulation Now →", type="primary", use_container_width=True, key="quick_simulate"):
            st.switch_page("pages/2_Simulation.py")
    with col_quick2:
        st.caption("Or continue managing personas below ↓")
    
    st.markdown("---")
else:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
    ">
        <h3 style="color: white; margin-top: 0;">👋 Get Started</h3>
        <p style="color: rgba(255,255,255,0.95); margin-bottom: 0;">
            Upload a CSV, create personas manually, or generate synthetic personas below!
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

# Create tabs (removed Connection tab since it's on Home page)
tab1, tab2, tab3 = st.tabs(["👥 Manage Personas", "🤖 Generate Personas", "⚙️ Simulation Settings"])

# Tab 1: Manage Personas
with tab1:
    st.header("Persona Management")
    
    # Create sub-tabs for different persona management methods
    persona_subtab1, persona_subtab2, persona_subtab3 = st.tabs([
        "📤 Upload from CSV",
        "➕ Create Manually",
        "📋 View/Manage Existing"
    ])
    
    # Use already loaded personas from top
    personas = disk_personas + session_personas
    
    # Sub-tab 1: Upload from CSV
    with persona_subtab1:
        st.subheader("Upload Personas from CSV File")
        st.write("Bulk import personas from a CSV file with demographic and background information.")
        
        # Show CSV format requirements
        with st.expander("📋 Required CSV Format"):
            st.markdown("""
            **Required Columns (minimum):**
            - `ID` or `name`: Unique identifier or full name
            - `age`: Age (number)
            - `gender`: Gender identity
            
            **Optional Columns** (all will be added as background information):
            - `occupation`: Job/profession
            - `education`: Education level
            - `location`: City/region  
            - `income`: Income level/range
            - `marital_status`: Marital status
            - `children`: Number of children
            - `health_status`: Current health condition
            - `political_affiliation`: Political views
            - `religion`: Religious affiliation
            - `personality_traits`: Comma or semicolon-separated
            - `values`: Comma or semicolon-separated
            - `interests`: Comma or semicolon-separated
            - `background`: Additional background text
            - *Any other column*: Will be added as background information
            
            **Example CSV (minimal):**
            ```
            ID,age,gender
            P001,45,Male
            P002,32,Female
            P003,28,Female
            ```
            
            **Example CSV (with optional fields):**
            ```
            ID,age,gender,occupation,education,location,health_status
            P001,45,Male,Teacher,Master's,Boston,Good
            P002,32,Female,Engineer,BS CS,SF,Excellent
            ```
            """)
            
            # Download template
            template_csv = """ID,age,gender,occupation,education,location,income,marital_status,children,health_status,personality_traits,values,interests,background
P001,45,Male,High School Teacher,Master's in Education,Boston MA,65000,Married,2,Good,patient;empathetic;dedicated,education;family;integrity,reading;hiking;teaching,"Has been teaching for 15 years"
P002,32,Female,Software Engineer,BS Computer Science,San Francisco CA,145000,Single,0,Excellent,analytical;creative;ambitious,innovation;work-life balance;growth,coding;travel;yoga,"Recently promoted to senior engineer"
P003,28,Female,Registered Nurse,Associate Degree Nursing,Miami FL,58000,Single,0,Good,compassionate;detail-oriented;calm,helping others;health;community,yoga;cooking;volunteering,"Works in emergency department"
P004,55,Male,Small Business Owner,MBA,Seattle WA,95000,Married,3,Fair,hardworking;practical;resilient,family;success;tradition,fishing;golf;mentoring,"Owns a local restaurant for 20 years"
P005,40,Female,Social Worker,MSW,Chicago IL,52000,Divorced,1,Good,empathetic;patient;strong,justice;empowerment;equality,activism;reading;community service,"Focuses on child welfare cases"
"""
            
            st.download_button(
                label="⬇️ Download CSV Template",
                data=template_csv,
                file_name="persona_template.csv",
                mime="text/csv",
                help="Download a pre-filled template to see the format"
            )
        
        # File uploader
        st.markdown("---")
        uploaded_file = st.file_uploader(
            "Choose CSV file",
            type=['csv'],
            help="Upload your CSV file with persona data"
        )
        
        if uploaded_file is not None:
            try:
                import pandas as pd
                
                # Read CSV
                df = pd.read_csv(uploaded_file)
                
                # Normalize column names
                df.columns = df.columns.str.strip().str.lower()
                
                # Check for ID or name column
                has_id = 'id' in df.columns
                has_name = 'name' in df.columns
                
                if not (has_id or has_name):
                    st.error("❌ CSV must have either 'ID' or 'name' column")
                elif 'age' not in df.columns:
                    st.error("❌ CSV must have 'age' column")
                elif 'gender' not in df.columns:
                    st.error("❌ CSV must have 'gender' column")
                else:
                    st.success(f"✅ CSV loaded! Found {len(df)} personas")
                    
                    with st.expander("👀 Preview Data"):
                        st.dataframe(df.head(10), use_container_width=True)
                    
                    # Import options
                    col_a, col_b = st.columns(2)
                    with col_a:
                        overwrite = st.checkbox(
                            "Overwrite existing personas",
                            value=False,
                            help="Replace personas with same name"
                        )
                    with col_b:
                        include_all = st.checkbox(
                            "Include all columns as background",
                            value=True,
                            help="Add all extra columns to persona background"
                        )
                    
                    # Import button
                    if st.button("📥 Import All Personas", type="primary", use_container_width=True):
                        success = 0
                        skipped = 0
                        errors = 0
                        
                        progress = st.progress(0)
                        status = st.empty()
                        
                        for idx, row in df.iterrows():
                            try:
                                # Get name from ID or name column
                                if 'id' in df.columns:
                                    person_name = str(row['id']).strip()
                                else:
                                    person_name = str(row['name']).strip()
                                
                                progress.progress((idx + 1) / len(df))
                                status.text(f"Processing {idx+1}/{len(df)}: {person_name}")
                                
                                # FLEXIBLE JSON CONVERSION: Convert ALL CSV columns to structured data
                                import json
                                
                                # Define core fields that become direct persona attributes
                                core_fields = ['id', 'name', 'age', 'gender']
                                optional_persona_fields = ['occupation', 'education', 'location']
                                list_fields = ['personality_traits', 'values', 'interests']
                                
                                # Build background as JSON string with ALL remaining columns
                                background_data = {}
                                traits = []
                                vals = []
                                
                                # Process all columns dynamically
                                for col in df.columns:
                                    if col in core_fields:
                                        continue  # Skip core fields
                                    
                                    if pd.notna(row[col]):
                                        # Handle list fields (traits, values, interests)
                                        if col == 'personality_traits':
                                            traits = [t.strip() for t in str(row[col]).replace(';', ',').split(',') if t.strip()]
                                        elif col == 'values':
                                            vals = [v.strip() for v in str(row[col]).replace(';', ',').split(',') if v.strip()]
                                        elif col == 'interests':
                                            background_data['interests'] = [i.strip() for i in str(row[col]).replace(';', ',').split(',') if i.strip()]
                                        # Handle optional persona fields
                                        elif col not in optional_persona_fields:
                                            # Add ALL other columns to background data
                                            # Clean column name for better readability
                                            clean_key = col.replace('_', ' ').title()
                                            background_data[col] = str(row[col]).strip()
                                
                                # Create a structured background string with key-value pairs
                                # This format is easily parsed back into JSON by the persona
                                bg_parts = []
                                for key, value in background_data.items():
                                    if isinstance(value, list):
                                        bg_parts.append(f"{key.replace('_', ' ').title()}: {', '.join(value)}")
                                    else:
                                        bg_parts.append(f"{key.replace('_', ' ').title()}: {value}")
                                
                                background = ". ".join(bg_parts) if bg_parts else "No additional background information provided"
                                
                                # Get optional fields with defaults
                                occupation = str(row['occupation']).strip() if 'occupation' in row and pd.notna(row['occupation']) else "Not specified"
                                education = str(row['education']) if 'education' in row and pd.notna(row['education']) else None
                                location = str(row['location']) if 'location' in row and pd.notna(row['location']) else None
                                
                                # Create persona - background will be automatically parsed to JSON by to_prompt_context
                                persona = Persona(
                                    name=person_name,
                                    age=int(row['age']),
                                    gender=str(row['gender']).strip(),
                                    occupation=occupation,
                                    background=background,
                                    personality_traits=traits if traits else [],
                                    values=vals if vals else [],
                                    education=education,
                                    location=location
                                )
                                
                                # Check if exists (in session personas only)
                                exists = any(p.name.lower() == persona.name.lower() for p in session_personas)
                                
                                if exists and not overwrite:
                                    skipped += 1
                                else:
                                    # Store in SESSION STATE ONLY (not saved to disk)
                                    st.session_state.session_personas.append(persona)
                                    success += 1
                                    
                            except Exception as e:
                                errors += 1
                                st.warning(f"Row {idx+1} ({row.get('name', 'unknown')}): {str(e)}")
                        
                        progress.empty()
                        status.empty()
                        
                        st.success(f"""
                        ✅ Import Complete!
                        - Imported: {success}
                        - Skipped: {skipped}
                        - Errors: {errors}
                        """)
                        
                        st.info("""
                        💡 **Session-Only Storage**: 
                        Uploaded personas are stored temporarily in your browser session.
                        They will be cleared when you close the browser.
                        Demo personas (saved to disk) remain permanent.
                        """)
                        
                        # Prominent confirmation button
                        if success > 0:
                            st.markdown("---")
                            col_a, col_b, col_c = st.columns([1, 2, 1])
                            with col_b:
                                if st.button("✅ Confirm & Continue to Simulation →", type="primary", use_container_width=True, key="confirm_csv"):
                                    st.switch_page("pages/2_Simulation.py")
                            st.markdown("---")
                            st.rerun()
                            
            except Exception as e:
                st.error(f"❌ Error reading CSV: {str(e)}")
    
    # Sub-tab 2: Create Manually
    with persona_subtab2:
        st.subheader("Create New Persona Manually")
        
        with st.form("new_persona_form"):
            name = st.text_input("Name *", placeholder="e.g., John Smith")
            
            col_x, col_y = st.columns(2)
            with col_x:
                age = st.number_input("Age *", min_value=18, max_value=100, value=30)
            with col_y:
                gender = st.text_input("Gender *", placeholder="e.g., Male, Female")
            
            occupation = st.text_input("Occupation *", placeholder="e.g., Software Engineer")
            education = st.text_input("Education", placeholder="e.g., Bachelor's in CS")
            location = st.text_input("Location", placeholder="e.g., New York, NY")
            
            background = st.text_area(
                "Background *",
                placeholder="Describe their life story, experiences, and context...",
                height=100
            )
            
            traits = st.text_input(
                "Personality Traits *",
                placeholder="Comma-separated: e.g., Analytical, Creative, Empathetic"
            )
            
            values = st.text_input(
                "Core Values *",
                placeholder="Comma-separated: e.g., Innovation, Honesty, Community"
            )
            
            submitted = st.form_submit_button("✨ Create Persona", type="primary", use_container_width=True)
            
            if submitted:
                # Validate
                if not all([name, age, gender, occupation, background, traits, values]):
                    st.error("Please fill in all required fields (*)")
                else:
                    # Parse traits and values
                    trait_list = [t.strip() for t in traits.split(',') if t.strip()]
                    value_list = [v.strip() for v in values.split(',') if v.strip()]
                    
                    # Create persona
                    new_persona = Persona(
                        name=name,
                        age=age,
                        gender=gender,
                        occupation=occupation,
                        background=background,
                        personality_traits=trait_list,
                        values=value_list,
                        education=education if education else None,
                        location=location if location else None
                    )
                    
                    # Save
                    if st.session_state.persona_manager.save_persona(new_persona):
                        st.success(f"✅ Created {name}!")
                        st.rerun()
                    else:
                        st.error("Failed to save persona")
    
    # Sub-tab 3: View/Manage Existing
    with persona_subtab3:
        st.subheader(f"Existing Personas ({len(personas)})")
        
        # Show counts
        col1, col2, col3 = st.columns(3)
        col1.metric("📁 Permanent (Demo)", len(disk_personas))
        col2.metric("🔄 Temporary (Uploaded)", len(session_personas))
        col3.metric("📊 Total", len(personas))
        
        st.info("""
        **Storage Info:**
        - **Permanent personas** (demo data) are saved to disk and persist across sessions
        - **Temporary personas** (CSV uploads) exist only in this browser session
        - Close browser → temporary personas are cleared, permanent remain
        """)
        
        if personas:
            # Add clear button for session personas
            if len(session_personas) > 0:
                if st.button(f"🗑️ Clear All Temporary Personas ({len(session_personas)})", type="secondary"):
                    st.session_state.session_personas = []
                    st.success("✅ Cleared all temporary personas")
                    st.rerun()
                st.markdown("---")
            
            # Display personas in expandable sections
            for persona in personas:
                # Determine if this is a disk or session persona
                is_disk_persona = persona in disk_personas
                storage_badge = "📁 Permanent" if is_disk_persona else "🔄 Temporary"
                
                with st.expander(f"**{persona.name}** - {persona.age} y/o {persona.occupation} `{storage_badge}`"):
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.write(f"**Storage:** {storage_badge}")
                        st.write(f"**Gender:** {persona.gender}")
                        st.write(f"**Age:** {persona.age}")
                        st.write(f"**Occupation:** {persona.occupation}")
                        if persona.education:
                            st.write(f"**Education:** {persona.education}")
                        if persona.location:
                            st.write(f"**Location:** {persona.location}")
                    
                    with col_b:
                        st.write("**Personality Traits:**")
                        for trait in persona.personality_traits:
                            st.write(f"- {trait}")
                        
                        st.write("**Values:**")
                        for value in persona.values:
                            st.write(f"- {value}")
                    
                    st.write(f"**Background:** {persona.background}")
                    
                    # Delete button - only for disk personas
                    if is_disk_persona:
                        filename = f"{persona.name.lower().replace(' ', '_')}.json"
                        if st.button(f"🗑️ Delete {persona.name}", key=f"delete_{filename}"):
                            if st.session_state.persona_manager.delete_persona(filename):
                                st.success(f"Deleted {persona.name}")
                                st.rerun()
                            else:
                                st.error(f"Failed to delete {persona.name}")
                    else:
                        st.caption("Temporary persona - will be cleared when browser closes")
        else:
            st.info("No personas found. Upload a CSV file or create personas manually.")

# Tab 2: Generate Personas
with tab2:
    st.header("🤖 Synthetic Persona Generation")
    st.markdown("""
    Generate large populations of synthetic personas using demographic distributions.
    Perfect for creating diverse, representative samples for testing.
    """)
    
    # Initialize persona generator
    if 'persona_generator' not in st.session_state:
        st.session_state.persona_generator = PersonaGenerator()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Population Size")
        n_personas = st.number_input(
            "Number of personas to generate:",
            min_value=10,
            max_value=1000,
            value=100,
            step=10,
            help="Larger populations provide more diverse samples but take longer to generate"
        )
    
    with col2:
        st.subheader("🎲 Random Seed")
        seed = st.number_input(
            "Random seed (for reproducibility):",
            min_value=1,
            max_value=999999,
            value=42,
            help="Same seed will generate identical personas"
        )
    
    st.markdown("---")
    
    # Distribution configuration
    st.subheader("📈 Demographic Distributions")
    
    # Age distribution
    col1, col2 = st.columns(2)
    with col1:
        age_dist = st.selectbox(
            "Age Distribution:",
            ["Normal (18-65)", "Uniform (18-65)", "Custom"],
            help="How ages should be distributed"
        )
    
    with col2:
        if age_dist == "Normal (18-65)":
            st.info("Mean: 40, Std: 12")
        elif age_dist == "Uniform (18-65)":
            st.info("Equal probability 18-65")
        else:
            st.info("Define custom distribution below")
    
    # Gender distribution
    col1, col2 = st.columns(2)
    with col1:
        gender_dist = st.selectbox(
            "Gender Distribution:",
            ["50/50 Male/Female", "60/40 Female/Male", "Custom"],
            help="Gender distribution in population"
        )
    
    with col2:
        if gender_dist == "50/50 Male/Female":
            st.info("50% Male, 50% Female")
        elif gender_dist == "60/40 Female/Male":
            st.info("60% Female, 40% Male")
        else:
            st.info("Define custom distribution below")
    
    # Education distribution
    col1, col2 = st.columns(2)
    with col1:
        education_dist = st.selectbox(
            "Education Distribution:",
            ["Realistic US", "High Education", "Custom"],
            help="Education level distribution"
        )
    
    with col2:
        if education_dist == "Realistic US":
            st.info("Based on US Census data")
        elif education_dist == "High Education":
            st.info("70% College+, 30% High School")
        else:
            st.info("Define custom distribution below")
    
    st.markdown("---")
    
    # Advanced settings
    with st.expander("🔧 Advanced Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            include_personality = st.checkbox("Generate personality traits", value=True)
            include_values = st.checkbox("Generate values", value=True)
            include_background = st.checkbox("Generate detailed backgrounds", value=True)
        
        with col2:
            realistic_names = st.checkbox("Use realistic names", value=True)
            diverse_occupations = st.checkbox("Diverse occupations", value=True)
            geographic_diversity = st.checkbox("Geographic diversity", value=True)
    
    st.markdown("---")
    
    # Generate button
    if st.button("🚀 Generate Personas", type="primary", use_container_width=True):
        if n_personas > 500:
            st.warning("⚠️ Large populations may take several minutes to generate")
        
        with st.spinner(f"Generating {n_personas} synthetic personas..."):
            try:
                # Clear existing distributions and add new ones
                st.session_state.persona_generator.distributions.clear()
                
                # Age distribution
                if age_dist == "Normal (18-65)":
                    st.session_state.persona_generator.add_distribution(DistributionConfig(
                        variable_name="age",
                        distribution_type="normal",
                        parameters={"mean": 40, "std": 12, "integer": True}
                    ))
                elif age_dist == "Uniform (18-65)":
                    st.session_state.persona_generator.add_distribution(DistributionConfig(
                        variable_name="age",
                        distribution_type="uniform",
                        parameters={"low": 18, "high": 65, "integer": True}
                    ))
                
                # Gender distribution
                if gender_dist == "50/50 Male/Female":
                    st.session_state.persona_generator.add_distribution(DistributionConfig(
                        variable_name="gender",
                        distribution_type="categorical",
                        parameters={"categories": ["Male", "Female"], "probabilities": [0.5, 0.5]}
                    ))
                elif gender_dist == "60/40 Female/Male":
                    st.session_state.persona_generator.add_distribution(DistributionConfig(
                        variable_name="gender",
                        distribution_type="categorical",
                        parameters={"categories": ["Female", "Male"], "probabilities": [0.6, 0.4]}
                    ))
                
                # Generate persona dictionaries
                persona_dicts = st.session_state.persona_generator.generate_personas(
                    n=n_personas,
                    include_background=include_background,
                    include_traits=include_personality,
                    include_values=include_values
                )
                
                # Convert dictionaries to Persona objects
                generated_personas = []
                for i, persona_dict in enumerate(persona_dicts):
                    try:
                        persona = Persona(
                            name=persona_dict.get('name', f'Generated Persona {i+1}'),
                            age=persona_dict.get('age', 30),
                            gender=persona_dict.get('gender', 'Other'),
                            occupation=persona_dict.get('occupation', 'Professional'),
                            background=persona_dict.get('background', 'Generated background'),
                            personality_traits=persona_dict.get('personality_traits', []),
                            values=persona_dict.get('values', []),
                            education=persona_dict.get('education', 'Bachelor\'s Degree'),
                            location=persona_dict.get('location', 'United States')
                        )
                        generated_personas.append(persona)
                    except Exception as e:
                        st.warning(f"Failed to create persona {i+1}: {str(e)}")
                        continue
                
                # Save to session state (temporary)
                if 'generated_personas' not in st.session_state:
                    st.session_state.generated_personas = []
                
                st.session_state.generated_personas.extend(generated_personas)
                
                st.success(f"✅ Generated {len(generated_personas)} synthetic personas!")
                
                # Show sample
                if generated_personas:
                    st.subheader("📋 Sample Generated Personas")
                    sample_size = min(5, len(generated_personas))
                    for i, persona in enumerate(generated_personas[:sample_size]):
                        with st.expander(f"Persona {i+1}: {persona.name}"):
                            st.write(f"**Age:** {persona.age}")
                            st.write(f"**Gender:** {persona.gender}")
                            st.write(f"**Occupation:** {persona.occupation}")
                            st.write(f"**Education:** {persona.education}")
                            st.write(f"**Location:** {persona.location}")
                            if persona.personality_traits:
                                st.write(f"**Personality:** {', '.join(persona.personality_traits[:3])}")
                    
                    # Prominent confirmation button
                    st.markdown("---")
                    col_a, col_b, col_c = st.columns([1, 2, 1])
                    with col_b:
                        if st.button("✅ Personas Ready - Continue to Simulation →", type="primary", use_container_width=True, key="confirm_generated"):
                            st.switch_page("pages/2_Simulation.py")
                    st.markdown("---")
                    
                    st.info("""
                    🎯 **These personas are ready to use!** 
                    
                    Click the button above to start running simulations, or save them permanently below.
                    Generated personas will appear in the persona selection list with [Generated] labels.
                    """)
                
                # Option to save permanently
                if st.button("💾 Save Generated Personas Permanently", type="secondary"):
                    saved_count = 0
                    for persona in generated_personas:
                        try:
                            st.session_state.persona_manager.save_persona(persona)
                            saved_count += 1
                        except Exception as e:
                            st.error(f"Failed to save {persona.name}: {str(e)}")
                    
                    st.success(f"✅ Saved {saved_count} personas permanently!")
                    st.rerun()
                
            except Exception as e:
                st.error(f"Failed to generate personas: {str(e)}")
                st.info("Make sure you're connected to an LLM (check Home page) for background generation")
    
    # Show current generated personas count
    if 'generated_personas' in st.session_state and st.session_state.generated_personas:
        st.markdown("---")
        st.subheader("📊 Current Generated Personas")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.metric("Generated Personas", len(st.session_state.generated_personas))
        
        with col2:
            if st.button("🗑️ Clear Generated Personas", type="secondary"):
                st.session_state.generated_personas = []
                st.rerun()
        
        st.info("Generated personas are temporary and will be cleared when you close the browser.")

# Tab 3: Simulation Settings
with tab3:
    st.header("Simulation Parameters")
    
    st.markdown("""
    Configure default parameters for your simulations. These can be adjusted per simulation.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Controls randomness. Lower = more focused, Higher = more creative"
        )
        
        st.session_state.default_temperature = temperature
    
    with col2:
        max_tokens = st.slider(
            "Max Tokens",
            min_value=50,
            max_value=2000,
            value=500,
            step=50,
            help="Maximum length of generated responses"
        )
        
        st.session_state.default_max_tokens = max_tokens
    
    st.info(f"""
    **Current Settings:**
    - Temperature: {temperature} ({"more creative" if temperature > 1.0 else "more focused" if temperature < 0.5 else "balanced"})
    - Max Tokens: {max_tokens} (~{max_tokens * 0.75:.0f} words)
    """)
    
    with st.expander("📖 Parameter Guide"):
        st.markdown("""
        ### Temperature
        - **0.0 - 0.3**: Very focused and deterministic responses
        - **0.4 - 0.7**: Balanced, good for most surveys
        - **0.8 - 1.2**: More creative and varied responses
        - **1.3 - 2.0**: Highly creative, potentially unpredictable
        
        ### Max Tokens
        - **50-150**: Short, concise answers
        - **200-500**: Standard responses (recommended)
        - **500-1000**: Detailed, elaborate responses
        - **1000+**: Very lengthy, comprehensive responses
        
        **Note**: 1 token ≈ 0.75 words on average
        """)

# Footer
st.markdown("---")
st.caption("💡 Tip: Create diverse personas to get varied perspectives in your simulations.")

