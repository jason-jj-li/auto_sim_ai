"""UI smoke tests — every page renders without exceptions, and the Simulation
wizard's Next gating works (step 3 blocks until questions are configured).

Uses streamlit.testing.v1.AppTest against the on-disk fixture personas/results.
Nav buttons are never clicked (switch_page is unsupported in AppTest).
"""
from streamlit.testing.v1 import AppTest
from src.persona import Persona


def _run(path):
    at = AppTest.from_file(path, default_timeout=30)
    at.run()
    assert not at.exception
    return at


def _next(at):
    return next(b for b in at.button if b.label.startswith("Next"))


def test_home_renders():
    at = _run("app.py")
    assert any(b.label == "Set up workspace →" for b in at.button)


def test_setup_renders_library():
    at = _run("pages/1_Setup.py")
    assert any(b.label == "Test connection" for b in at.button)
    assert any("Add personas" in b.label for b in at.button)


def test_results_renders():
    at = _run("pages/3_Results.py")
    assert at.selectbox  # run selector present (fixtures on disk)


def test_simulation_step1_renders():
    # NOTE: only one .run() here — AppTest mis-collects st.segmented_control's
    # widget state on the *second* run (single-value string iterated as chars).
    at = _run("pages/2_Simulation.py")
    assert any("Simulation progress" in m.value for m in at.markdown)
    assert not _next(at).disabled


def test_simulation_wizard_gating():
    at = AppTest.from_file("pages/2_Simulation.py", default_timeout=30)
    at.session_state["sim_step"] = 2
    at.session_state["session_personas"] = [Persona(
        name="Fixture Person", age=30, gender="X", occupation="Tester",
        background="UI fixture", personality_traits=[], values=[]
    )]
    at.run()
    assert not at.exception
    assert at.multiselect and len(at.multiselect[0].value) > 0  # fixtures pre-selected
    assert not _next(at).disabled
    _next(at).click().run()  # step 2 → 3
    assert not at.exception
    assert _next(at).disabled  # step 3: no questions configured yet


def test_simulation_step4_offers_home_link_without_model():
    at = AppTest.from_file("pages/2_Simulation.py", default_timeout=30)
    at.session_state["sim_step"] = 4
    at.run()
    assert not at.exception
    assert any("connect a model" in c.value for c in at.caption)
    assert any("Go to Home" in b.label for b in at.button)
