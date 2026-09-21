"""Setup page for persona and configuration management."""
import streamlit as st
import json
from src import Persona, PersonaManager, personas_from_dataframe, render_navigation, render_page_header, section, stat_cards, render_empty_state, render_model_connection, PersonaGenerator, DistributionConfig
from src.styles import apply_global_styles

st.set_page_config(page_title="Setup - LLM Simulation", page_icon="A", layout="wide", initial_sidebar_state="collapsed")

# Apply global design system
apply_global_styles()

# Top Navigation
render_navigation(current_page="setup")

render_page_header(
    "Workspace setup",
    "Connect the execution model, then generate a synthetic population or import respondent data.",
    eyebrow="Setup",
)

# Initialize session state if needed
if 'persona_manager' not in st.session_state:
    st.session_state.persona_manager = PersonaManager()
if 'persona_generator' not in st.session_state:
    st.session_state.persona_generator = PersonaGenerator()
if 'llm_client' not in st.session_state:
    st.session_state.llm_client = None
if 'base_url' not in st.session_state:
    st.session_state.base_url = "http://localhost:1234/v1"

section("1 · Model & execution", first=True)
render_model_connection()

# Initialize session-only personas (uploaded personas, cleared on browser close)
if 'session_personas' not in st.session_state:
    st.session_state.session_personas = []  # Temporary personas from CSV upload

# Population workspace
section("2 · Population")
disk_personas = st.session_state.persona_manager.load_all_personas()
session_personas = st.session_state.get('session_personas', [])
generated_personas = st.session_state.get('generated_personas', [])
total_personas = len(disk_personas) + len(session_personas) + len(generated_personas)

if total_personas > 0:
    stat_cards([
        ("Total", total_personas),
        ("Permanent", len(disk_personas)),
        ("Temporary", len(session_personas)),
        ("Generated", len(generated_personas)),
    ])
    if st.button("Go to Simulation →", type="primary", key="quick_simulate"):
        st.switch_page("pages/2_Simulation.py")
    st.markdown("---")
else:
    st.caption("Get started: generate a synthetic population with AI extraction, or upload a CSV of personas.")

# Persona library — the main view (add via the dialog below)
personas = disk_personas + session_personas + generated_personas
section("Persona library")
st.caption("Permanent personas persist on disk; uploaded and generated personas live only in this browser session.")

if personas:
    import pandas as pd

    # one row per persona; source derived from pool boundaries (index ranges, not equality)
    n_disk, n_sess = len(disk_personas), len(session_personas)
    rows = []
    for i, p in enumerate(personas):
        rows.append({
            "ID": p.persona_id,
            "Name": p.name,
            "Age": p.age,
            "Gender": str(p.gender),
            "Occupation": str(p.occupation),
            "Education": p.education or "",
            "Location": p.location or "",
            "Source": "Permanent" if i < n_disk else ("Temporary" if i < n_disk + n_sess else "Generated"),
        })
    df_all = pd.DataFrame(rows)

    f1, f2 = st.columns([2, 1])
    with f1:
        search = st.text_input("Search personas", placeholder="Search name, occupation, location…",
                               label_visibility="collapsed")
    with f2:
        src_filter = st.multiselect("Source", ["Permanent", "Temporary", "Generated"],
                                    placeholder="All sources")
    mask = pd.Series(True, index=df_all.index)
    if search.strip():
        q = search.strip().lower()
        mask &= df_all[["Name", "Occupation", "Location", "Gender"]].apply(
            lambda c: c.str.lower().str.contains(q, na=False)).any(axis=1)
    if src_filter:
        mask &= df_all["Source"].isin(src_filter)
    df_view = df_all[mask]

    event = st.dataframe(
        df_view,
        use_container_width=True,
        hide_index=True,
        height=420,
        on_select="rerun",
        selection_mode="multi-row",
        key="persona_table",
    )
    sel_idx = [df_view.index[i] for i in event.selection.rows]  # positions in `personas`

    if sel_idx:
        a1, a2, _ = st.columns([1, 1, 2])
        with a1:
            if st.button(f"Save {len(sel_idx)} to permanent",
                         disabled=all(df_all.loc[i, "Source"] == "Permanent" for i in sel_idx)):
                saved = 0
                for i in sel_idx:
                    p = personas[i]
                    if st.session_state.persona_manager.save_persona(p):
                        saved += 1
                        # remove from the session pool it came from, else it shows twice
                        if n_disk <= i < n_disk + n_sess:
                            st.session_state.session_personas.remove(p)
                        elif i >= n_disk + n_sess and 'generated_personas' in st.session_state:
                            st.session_state.generated_personas.remove(p)
                st.toast(f"Saved {saved} personas permanently")
                st.rerun()
        with a2:
            if st.button(f"Delete {len(sel_idx)} selected", type="secondary"):
                for i in sel_idx:
                    p = personas[i]
                    if i < n_disk:
                        st.session_state.persona_manager.delete_persona(p.persona_id)
                    elif i < n_disk + n_sess:
                        st.session_state.session_personas.remove(p)
                    elif 'generated_personas' in st.session_state:
                        st.session_state.generated_personas.remove(p)
                st.toast(f"Deleted {len(sel_idx)} personas")
                st.rerun()

    # single-selection detail pane
    if len(sel_idx) == 1:
        p = personas[sel_idx[0]]
        with st.expander(f"{p.name} — details", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Age:** {p.age}  **Gender:** {p.gender}")
                st.write(f"**Occupation:** {p.occupation}")
                if p.education:
                    st.write(f"**Education:** {p.education}")
                if p.location:
                    st.write(f"**Location:** {p.location}")
            with c2:
                if p.personality_traits:
                    st.write(f"**Traits:** {', '.join(map(str, p.personality_traits))}")
                if p.values:
                    st.write(f"**Values:** {', '.join(map(str, p.values))}")
            st.write(f"**Background:** {p.background}")
            extras = getattr(p, '_extra_attributes', None) or {}
            if extras:
                st.caption(" · ".join(f"**{k.replace('_', ' ').title()}:** {v}"
                                      for k, v in extras.items() if v is not None))

    if session_personas or generated_personas:
        if st.button("Clear all temporary & generated", type="secondary"):
            st.session_state.session_personas = []
            st.session_state.generated_personas = []
            st.toast("Cleared session personas")
            st.rerun()
else:
    render_empty_state(
        "No personas yet",
        "Generate a population from a plain-language brief or upload a CSV to begin.",
        icon="◎",
    )

@st.dialog("Add personas", width="large")
def add_personas_dialog():
    d1, d2 = st.tabs(["Generate — AI extraction", "Upload CSV"])
    with d2:
        st.markdown("**Upload Personas from CSV File**")
        st.write("Bulk import personas from a CSV file with demographic and background information.")

        # Show CSV format requirements
        with st.expander("How columns are parsed"):
            st.markdown("""
            **No required columns — any CSV works.** Columns are auto-detected (case-insensitive):

            - `name` / `id` / `姓名` → persona name (missing → auto-generated)
            - `age` / `年龄` → age (a range like `25-34` takes the midpoint; missing → 30)
            - `gender` / `性别`, `occupation` / `职业`, `education`, `location`, `marital_status`,
              `ethnicity`, `political_affiliation`, `religion`, `background` → the matching persona fields
            - `personality_traits`, `values` → split on `,` `;` `、` into lists
            - **every other column** → kept as a custom attribute, shown on the persona card
              and included in the LLM prompt
            """)
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
                df = pd.read_csv(uploaded_file)
                st.caption(f"CSV loaded — {len(df)} rows. Columns are parsed automatically on import.")
                with st.expander("Preview Data"):
                    st.dataframe(df.head(10), use_container_width=True)

                overwrite = st.checkbox("Overwrite personas with the same CSV ID", value=False)
                if st.button("Import All Personas", type="primary", use_container_width=True):
                    new_personas = personas_from_dataframe(df)
                    existing = {p.persona_id for p in st.session_state.session_personas}
                    success = skipped = 0
                    for p in new_personas:
                        key = p.persona_id
                        if key in existing:
                            if not overwrite:
                                skipped += 1
                                continue
                            st.session_state.session_personas = [
                                x for x in st.session_state.session_personas if x.persona_id != key]
                        st.session_state.session_personas.append(p)
                        existing.add(key)
                        success += 1
                    st.caption(f"Import complete — {success} imported, {skipped} skipped (duplicate names). "
                               "Stored for this browser session only.")
                    if success > 0:
                        if st.button("Confirm & Continue to Simulation →", type="primary",
                                     use_container_width=True, key="confirm_csv"):
                            st.switch_page("pages/2_Simulation.py")
            except Exception as e:
                st.error(f"Error reading CSV: {str(e)}")

    # Sub-tab 1: AI extraction (primary)
    with d1:
        st.markdown("**AI Demographic Extraction**")
        st.markdown("""
        Paste any text describing your target population, and AI will automatically extract
        key demographic information to generate personas.

        **Examples:**
        - Research study descriptions
        - Survey target audience descriptions
        - Marketing segment descriptions
        - Population characteristics from reports
        """)

        # Check if LLM is connected
        if not st.session_state.llm_client:
            st.warning("LLM not connected. Please connect on the Home page first.")
            st.caption("Go to **Home page** → Enter API URL → Click 'Test Connection'")
        else:
            st.caption(f"LLM Connected: {st.session_state.selected_model}")

        st.markdown("---")

        # Text input area
        ai_text_input = st.text_area(
            "Paste your population description here:",
            placeholder="""Example:
We're studying college students aged 18-24 in California universities.
The population is approximately 60% female and 40% male, mostly majoring
in STEM fields (Computer Science, Engineering, Biology). Most are from
middle to upper-middle-class families with household incomes between
$75,000-$150,000. They value education, career success, and work-life
balance. Common interests include technology, social media, fitness,
and environmental sustainability.""",
            height=200,
            help="Paste any text describing the demographic characteristics of your target population"
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            ai_n_personas = st.number_input(
                "Number of personas to generate:",
                min_value=5,
                max_value=None,
                value=50,
                step=5,
                help="How many personas to create from the extracted demographics",
                key="ai_n_personas"
            )

        with col2:
            ai_seed = st.number_input(
                "Random seed:",
                min_value=1,
                max_value=999999,
                value=42,
                help="For reproducible results",
                key="ai_seed"
            )

        # Advanced options
        with st.expander("Advanced Options"):
            ai_max_tokens = st.slider(
                "Max tokens for AI extraction",
                min_value=500,
                max_value=32000,
                value=4000,
                step=500,
                help="Token budget for the AI's extraction reply. Reasoning models (deepseek-reasoner/flash) "
                     "spend their THINKING tokens out of this same budget — if extraction fails with "
                     "'finish_reason=length', the model used it all before writing the JSON; raise this. "
                     "4000–8000 covers most cases.",
                key="ai_extract_max_tokens"
            )
            use_llm_parser = st.checkbox(
                "Enable LLM Universal Parser",
                value=True,
                help="""
                When enabled, the system uses LLM to automatically parse new variables in your prompt.

                Benefits:
                - No need to pre-write parsers for each new field
                - Automatically identifies fields with categories and percentages
                - Flexibly adapts to various expression styles

                Example: If your prompt contains "exercise habits: frequent 35%, occasional 45%, never 20%",
                the system will automatically convert it to an exercise_habit categorical variable.

                Note: Enabling this option increases LLM calls (one call per unknown field).
                """
            )

            st.caption("**Tip**: With the universal parser enabled, you can add any new variables in your population description (e.g., exercise habits, dietary preferences), and the system will automatically identify and create corresponding categorical variables.")

        # Step 1: Extract demographics with AI
        if st.button("Extract Demographics", type="primary", use_container_width=True, disabled=not st.session_state.llm_client):
            if not ai_text_input.strip():
                st.error("Please enter some text describing your population")
            else:
                with st.spinner("AI is analyzing the text and extracting demographic information..."):
                    extracted_data = PersonaGenerator.extract_demographics_with_ai(
                        text_input=ai_text_input,
                        llm_client=st.session_state.llm_client,
                        model=st.session_state.selected_model,
                        max_tokens=ai_max_tokens
                    )

                # Check for errors
                if "error" in extracted_data:
                    st.error(f"AI extraction failed: {extracted_data['error']}")
                    if "raw_response" in extracted_data:
                        with st.expander("View AI Response (for debugging)"):
                            st.code(extracted_data['raw_response'])
                    st.session_state.pop('ai_extracted', None)
                else:
                    st.session_state.ai_extracted = extracted_data
                    st.session_state.pop('ai_dist_editor', None)  # drop edits from any previous extraction

        # Step 2: review the parsed distributions (edit probabilities if needed), then generate
        ai_extracted = st.session_state.get('ai_extracted')
        if ai_extracted:
            st.caption("Successfully extracted demographic information!")

            dists = ai_extracted.get('distributions')
            dists = dists if isinstance(dists, dict) else {}
            other_info = {k: v for k, v in ai_extracted.items()
                          if k not in ('distributions', 'error', 'raw_response') and v is not None}
            if other_info:
                st.caption(" · ".join(f"**{k.replace('_', ' ').title()}:** {v}" for k, v in other_info.items()))

            if dists:
                import pandas as pd
                st.markdown("**Review extracted distributions** — edit probabilities before generating")
                flat_rows = []
                for field, spec in dists.items():
                    if not isinstance(spec, dict):
                        continue
                    parent = spec.get('conditioned_on')
                    table = spec.get('table')
                    if parent and isinstance(table, dict):
                        # conditional field: one block of rows per parent category
                        for when, sub in table.items():
                            if not isinstance(sub, dict):
                                continue
                            cats = sub.get('categories') or []
                            probs = sub.get('probabilities') or []
                            for i, cat in enumerate(cats):
                                p = probs[i] if i < len(probs) and isinstance(probs[i], (int, float)) else None
                                flat_rows.append({"Field": field, "When": f"{parent}={when}", "Category": str(cat),
                                                  "Probability (%)": round(p * 100, 1) if p is not None else None})
                        continue
                    cats = spec.get('categories') or []
                    probs = spec.get('probabilities') or []
                    for i, cat in enumerate(cats):
                        p = probs[i] if i < len(probs) and isinstance(probs[i], (int, float)) else None
                        flat_rows.append({"Field": field, "When": "", "Category": str(cat),
                                          "Probability (%)": round(p * 100, 1) if p is not None else None})
                if flat_rows:
                    edited_df = st.data_editor(
                        pd.DataFrame(flat_rows),
                        disabled=["Field", "When", "Category"],
                        column_config={"Probability (%)": st.column_config.NumberColumn(min_value=0.0, max_value=100.0, step=0.5)},
                        use_container_width=True,
                        key="ai_dist_editor"
                    )
                    # Rebuild distributions from the (possibly edited) table;
                    # blank/invalid cells become 0 -> all-zero field falls back to uniform downstream
                    rebuilt: dict = {}
                    for row in edited_df.to_dict('records'):
                        p = row["Probability (%)"]
                        pv = float(p) / 100.0 if p is not None else 0.0
                        when = row.get("When") or ""
                        if '=' in when:
                            parent, parent_cat = when.split('=', 1)
                            tbl = rebuilt.setdefault(row["Field"], {"conditioned_on": parent, "table": {}})["table"]
                            entry = tbl.setdefault(parent_cat, {"categories": [], "probabilities": []})
                        else:
                            entry = rebuilt.setdefault(row["Field"], {"categories": [], "probabilities": []})
                        entry["categories"].append(row["Category"])
                        entry["probabilities"].append(pv)
                    ai_extracted = {**ai_extracted, "distributions": rebuilt}

            with st.expander("Extracted Demographics (raw JSON)"):
                st.json(st.session_state.ai_extracted)

            # Step 3: Generate personas based on extracted data
            if st.button(f"Generate {ai_n_personas} Personas", type="primary", use_container_width=True, key="generate_from_ai_extract"):
                with st.spinner(f"Generating {ai_n_personas} personas from extracted demographics..."):
                    try:
                        persona_dicts = PersonaGenerator.generate_personas_from_ai_extraction(
                            extracted_data=ai_extracted,
                            n=ai_n_personas,
                            seed=ai_seed,
                            use_llm_parser=use_llm_parser,
                            llm_client=st.session_state.llm_client if use_llm_parser else None,
                            model=st.session_state.selected_model if use_llm_parser else "gpt-4o-mini"
                        )

                        # Convert dictionaries to Persona objects
                        generated_personas = []
                        for i, persona_dict in enumerate(persona_dicts):
                            try:
                                # Use from_dict to preserve all fields including dynamic ones
                                persona = Persona.from_dict(persona_dict)
                                generated_personas.append(persona)
                            except Exception as e:
                                st.warning(f"Failed to create persona {i+1}: {str(e)}")
                                continue

                        # Save to session state
                        st.session_state.generated_personas = generated_personas

                        st.caption(f"Generated {len(generated_personas)} personas from AI-extracted demographics!")

                        # Demographic Summary Table
                        st.markdown("**Population Demographics Summary**")

                        # Calculate statistics
                        import pandas as pd
                        from collections import Counter

                        # Get all persona dicts for processing
                        persona_dicts = [p.to_dict() for p in generated_personas]

                        # Collect all fields and their distributions
                        all_variable_stats = []

                        # 1. Age (special handling - continuous variable)
                        ages = [p.age for p in generated_personas]
                        age_mean = sum(ages) / len(ages)
                        age_min = min(ages)
                        age_max = max(ages)
                        all_variable_stats.append({
                            "Variable Name": "Age",
                            "Type": "Continuous",
                            "Distribution": f"Mean={age_mean:.1f}, Range=[{age_min}, {age_max}]"
                        })

                        # 2. Collect all categorical fields
                        # Standard fields to check
                        categorical_fields = {
                            'gender': 'Gender',
                            'occupation': 'Occupation',
                            'education': 'Education',
                            'location': 'Location',
                            'marital_status': 'Marital Status',
                            'ethnicity': 'Ethnicity',
                            'political_affiliation': 'Political Affiliation',
                            'religion': 'Religion',
                            'health_status': 'Health Status',
                            'income_range': 'Income Range',
                            'children': 'Children',
                            'social_insurance': 'Social Insurance',
                            'family_structure': 'Family Structure',
                            'tech_usage': 'Tech Usage'
                        }

                        # Find all additional dynamic fields not in the standard list
                        all_fields = set()
                        for p_dict in persona_dicts:
                            all_fields.update(p_dict.keys())

                        # Exclude non-demographic fields
                        excluded_fields = {'name', 'background', 'personality_traits', 'values', 'interests'}
                        dynamic_fields = all_fields - set(categorical_fields.keys()) - excluded_fields - {'age'}

                        # Add dynamic fields to categorical_fields dict
                        for field in sorted(dynamic_fields):
                            field_display = field.replace('_', ' ').title()
                            categorical_fields[field] = field_display

                        # Calculate distributions for all categorical fields
                        for field, display_name in sorted(categorical_fields.items(), key=lambda x: x[1]):
                            field_values = []

                            # Handle different field sources
                            if field == 'gender':
                                field_values = [
                                    p.gender if isinstance(p.gender, str) else str(p.gender)
                                    for p in generated_personas
                                ]
                            elif field == 'occupation':
                                field_values = [
                                    p.occupation if isinstance(p.occupation, str) else
                                    (', '.join(p.occupation) if isinstance(p.occupation, list) else str(p.occupation))
                                    for p in generated_personas
                                ]
                            elif field == 'education':
                                field_values = [
                                    p.education if isinstance(p.education, str) else
                                    (', '.join(p.education) if isinstance(p.education, list) else str(p.education))
                                    for p in generated_personas if p.education
                                ]
                            elif field == 'location':
                                field_values = [
                                    p.location if isinstance(p.location, str) else
                                    (', '.join(p.location) if isinstance(p.location, list) else str(p.location))
                                    for p in generated_personas if p.location
                                ]
                            else:
                                # Get from dict
                                field_values = [
                                    str(d.get(field)) for d in persona_dicts
                                    if d.get(field) is not None
                                ]

                            if field_values:
                                counts = Counter(field_values)
                                total = len(field_values)

                                # Format distribution string (top 5 categories)
                                dist_parts = []
                                for value, count in counts.most_common(5):
                                    pct = (count / total) * 100
                                    # Truncate long values
                                    display_value = value[:15] + "..." if len(value) > 15 else value
                                    dist_parts.append(f"{display_value} ({pct:.1f}%)")

                                if len(counts) > 5:
                                    dist_parts.append(f"...+{len(counts)-5} more")

                                dist_str = ", ".join(dist_parts)

                                all_variable_stats.append({
                                    "Variable Name": display_name,
                                    "Type": "Categorical",
                                    "Distribution": dist_str
                                })

                        # Display as table
                        if all_variable_stats:
                            df_stats = pd.DataFrame(all_variable_stats)
                            st.dataframe(df_stats, use_container_width=True, height=400)

                            st.caption(f"Successfully generated {len(all_variable_stats)} demographic variables")

                            # Add download button for the statistics
                            csv = df_stats.to_csv(index=False, encoding='utf-8-sig')
                            st.download_button(
                                label="Download Variable Statistics",
                                data=csv,
                                file_name="population_demographics_summary.csv",
                                mime="text/csv"
                            )

                        st.markdown("---")

                        # Show samples
                        st.markdown("**Sample Generated Personas**")
                        sample_size = min(5, len(generated_personas))

                        for i, persona in enumerate(generated_personas[:sample_size]):
                            with st.expander(f"Persona {i+1}: {persona.name}"):
                                col_p1, col_p2 = st.columns(2)

                                # Get all persona attributes
                                persona_dict = persona.to_dict() if hasattr(persona, 'to_dict') else vars(persona)

                                # Core demographic fields (left column)
                                with col_p1:
                                    st.write(f"**Age:** {persona.age}")
                                    st.write(f"**Gender:** {persona.gender}")
                                    st.write(f"**Occupation:** {persona.occupation}")
                                    if persona.education:
                                        st.write(f"**Education:** {persona.education}")
                                    if persona.location:
                                        st.write(f"**Location:** {persona.location}")

                                    # Additional demographic fields from dict
                                    if persona_dict.get('marital_status'):
                                        st.write(f"**Marital Status:** {persona_dict['marital_status']}")
                                    if persona_dict.get('ethnicity'):
                                        st.write(f"**Ethnicity:** {persona_dict['ethnicity']}")
                                    if persona_dict.get('political_affiliation'):
                                        st.write(f"**Political:** {persona_dict['political_affiliation']}")
                                    if persona_dict.get('religion'):
                                        st.write(f"**Religion:** {persona_dict['religion']}")

                                # Personality and additional info (right column)
                                with col_p2:
                                    if persona.personality_traits:
                                        st.write(f"**Personality:** {', '.join(persona.personality_traits[:3])}")
                                    if persona.values:
                                        st.write(f"**Values:** {', '.join(persona.values[:3])}")

                                    # Show other custom fields
                                    standard_fields = {'name', 'age', 'gender', 'occupation', 'education',
                                                     'location', 'background', 'personality_traits', 'values',
                                                     'marital_status', 'ethnicity', 'political_affiliation', 'religion'}

                                    for key, value in persona_dict.items():
                                        if key not in standard_fields and value and str(value).strip():
                                            # Format field name
                                            field_name = key.replace('_', ' ').title()
                                            # Truncate long values
                                            value_str = str(value)
                                            if len(value_str) > 50:
                                                value_str = value_str[:47] + "..."
                                            st.write(f"**{field_name}:** {value_str}")

                                st.write(f"**Background:** {persona.background[:200]}...")

                        # Action buttons
                        st.markdown("---")
                        col_act1, col_act2 = st.columns(2)

                        with col_act1:
                            if st.button("Personas Ready - Continue to Simulation →", type="primary", use_container_width=True, key="confirm_ai_generated"):
                                st.switch_page("pages/2_Simulation.py")

                        with col_act2:
                            if st.button("Save Generated Personas Permanently", type="secondary", use_container_width=True, key="save_ai_generated"):
                                saved_count = 0
                                for persona in generated_personas:
                                    try:
                                        st.session_state.persona_manager.save_persona(persona)
                                        saved_count += 1
                                    except Exception as e:
                                        st.error(f"Failed to save {persona.name}: {str(e)}")
                                if saved_count:
                                    st.session_state.generated_personas = []
                                st.toast(f"Saved {saved_count} personas permanently!")
                                st.rerun()

                        st.markdown("---")
                        st.caption("""
                        **These personas are ready to use!**

                        - Generated personas will appear in the persona selection list during simulation
                        - They are stored temporarily and will be cleared when you close the browser
                        - Click "Save Permanently" above to keep them across sessions
                        """)

                    except Exception as e:
                        st.error(f"Failed to generate personas: {str(e)}")
                        import traceback
                        with st.expander("Error Details"):
                            st.code(traceback.format_exc())

        # Show Continue button if personas were generated (outside the if block)
        if 'generated_personas' in st.session_state and st.session_state.generated_personas:
            st.markdown("---")
            st.markdown("**Generated Personas Ready!**")
            st.caption(f"**{len(st.session_state.generated_personas)} personas** have been generated and are ready to use.")

            col_ready1, col_ready2 = st.columns(2)
            with col_ready1:
                if st.button("Continue to Simulation →", type="primary", use_container_width=True, key="continue_from_ai_extract"):
                    st.switch_page("pages/2_Simulation.py")

            with col_ready2:
                if st.button("Clear Generated Personas", type="secondary", use_container_width=True, key="clear_ai_extract"):
                    st.session_state.generated_personas = []
                    st.rerun()

        # Tips section
        st.markdown("---")
        with st.expander("Tips for Best Results"):
            st.markdown("""
            **What to Include in Your Description:**
            - Age range or average age
            - Gender distribution
            - Occupation or professional field
            - Education level
            - Geographic location
            - Income level or socioeconomic status
            - Interests and hobbies
            - Values and beliefs
            - Any other relevant demographic characteristics

            **Example Descriptions:**

            1. **Healthcare Study:**
            > "Nurses and healthcare workers, ages 28-55, primarily female (80%),
            > working in urban hospitals. Most have bachelor's or associate degrees in nursing.
            > They value patient care, work-life balance, and professional development.
            > Common challenges include long hours and high stress."

            2. **Consumer Research:**
            > "Tech-savvy millennials aged 25-40, mixed gender, living in major metropolitan
            > areas. Most have college degrees and work in white-collar professions with
            > incomes between $60K-$120K. They value convenience, sustainability, and
            > social responsibility. Heavy users of smartphones and social media."

            3. **Educational Research:**
            > "High school teachers, ages 30-60, mixed gender, teaching in suburban
            > public schools. Most have master's degrees in education. They're passionate
            > about student success but concerned about limited resources and administrative
            > burden. Value creativity, student engagement, and professional autonomy."
            """)

    # Sub-tab 2: Statistical Distributions (existing code)


if st.button("＋ Add personas", type="primary"):
    add_personas_dialog()
