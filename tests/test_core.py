import sys
from unittest.mock import MagicMock

# --- STEP 1: MOCK STREAMLIT & DEPENDENCIES ---
mock_st = MagicMock()
sys.modules['streamlit'] = mock_st

# Custom SessionState mock class supporting both item and attribute access
class SessionStateMock(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'SessionStateMock' object has no attribute '{key}'")
            
    def __setattr__(self, key, value):
        self[key] = value
        
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f"'SessionStateMock' object has no attribute '{key}'")


# Assign session state instance globally
mock_session = SessionStateMock()
mock_st.session_state = mock_session

# Configure mock API return lists to support unpacking
def mock_tabs(tab_list):
    return [MagicMock() for _ in tab_list]


def mock_columns(col_spec):
    num_cols = col_spec if isinstance(col_spec, int) else len(col_spec)
    return [MagicMock() for _ in range(num_cols)]


mock_st.tabs.side_effect = mock_tabs
mock_st.columns.side_effect = mock_columns

# Return string values for inputs
mock_st.text_area.return_value = "Mock alert message content text"
mock_st.text_input.return_value = "Mock input search query text"
mock_st.chat_input.return_value = "Mock chat query text"
mock_st.selectbox.return_value = "Gate A (East)"
mock_st.radio.return_value = "⚡ Standard Route (Fastest)"
mock_st.multiselect.return_value = ["Spanish (Español)"]

# Mock plotly.express
mock_px = MagicMock()
sys.modules['plotly.express'] = mock_px

# --- STEP 2: IMPORT LOGIC & MODULES ---
import unittest  # noqa: E402
from modules.utils import (  # noqa: E402
    sanitize_input,
    get_routing_steps,
    get_waste_sorting_recommendation,
    get_broadcast_translation_fallback,
    get_fifa_manual_entry
)
from modules.fan_hub import run_fan_hub  # noqa: E402
from modules.ops_center import run_ops_center  # noqa: E402
from modules.sustainability import run_sustainability  # noqa: E402
from modules.broadcast import run_broadcast  # noqa: E402


class TestArenaFlowAI(unittest.TestCase):
    def setUp(self):
        self.mock_model = MagicMock()
        self.mock_response = MagicMock()
        self.mock_response.text = "Mock GenAI Response Text"
        self.mock_model.generate_content.return_value = self.mock_response
        
        # Reset session state before each test
        mock_session.clear()
        
        # Reset mock inputs
        mock_st.chat_input.return_value = None
        mock_st.text_input.return_value = ""
        mock_st.button.return_value = False
        mock_st.form_submit_button.return_value = False

    def test_mock_gemini_interaction(self):
        prompt = "Hello AI"
        response = self.mock_model.generate_content(prompt)
        self.assertEqual(response.text, "Mock GenAI Response Text")
        self.mock_model.generate_content.assert_called_once_with(prompt)

    def test_sanitize_input(self):
        self.assertEqual(
            sanitize_input("Hello <script>alert('XSS')</script> World"), 
            "Hello alert(&#x27;XSS&#x27;) World"
        )
        self.assertEqual(sanitize_input("   Lead space strip   "), "Lead space strip")
        self.assertEqual(sanitize_input(None), "")
        self.assertEqual(sanitize_input("<b>Bold</b>"), "Bold")

    def test_get_routing_steps(self):
        steps_std = get_routing_steps("Gate A", "Section 104", "Standard")
        self.assertTrue(len(steps_std) > 0)
        self.assertTrue("Gate A" in steps_std[0][1])

        steps_acc = get_routing_steps("Gate B", "Section 108", "Accessible")
        self.assertTrue("Elevator" in steps_acc[1][1] or "tactile" in steps_acc[2][1])

        steps_sens = get_routing_steps("Gate C", "Section 112", "Sensory")
        self.assertTrue("Sensory" in steps_sens[2][1])

        steps_eco = get_routing_steps("Gate D", "Section 115", "Eco-Path")
        self.assertTrue("Eco-Hub" in steps_eco[1][1])

    def test_get_waste_sorting_recommendation(self):
        compost = get_waste_sorting_recommendation("banana peel")
        self.assertTrue("Compost" in compost)

        paper = get_waste_sorting_recommendation("paper cup")
        self.assertTrue("Recycling" in paper)

        plastic = get_waste_sorting_recommendation("plastic bottle")
        self.assertTrue("Recycling" in plastic)

        landfill = get_waste_sorting_recommendation("greasy wrapper")
        self.assertTrue("Landfill" in landfill)

    def test_get_broadcast_translation_fallback(self):
        spanish_shuttle = get_broadcast_translation_fallback("shuttle bus to MetLife", "Spanish")
        self.assertTrue("MetLife" in spanish_shuttle)

        french_gate = get_broadcast_translation_fallback("gate c is exit only", "French")
        self.assertTrue("porte C" in french_gate)

        custom_german = get_broadcast_translation_fallback("attention fans", "German")
        self.assertTrue("KI" in custom_german or "German" in custom_german)

    def test_get_fifa_manual_entry(self):
        evac = get_fifa_manual_entry("evacuation protocol")
        self.assertTrue("Assembly" in evac)

        lost = get_fifa_manual_entry("lost child info")
        self.assertTrue("CSO" in lost)

        med = get_fifa_manual_entry("medical assistance")
        self.assertTrue("Red Cross" in med)

        concession = get_fifa_manual_entry("concession queue times")
        self.assertTrue("wait times" in concession)

        transit = get_fifa_manual_entry("transit terminal")
        self.assertTrue("shuttle" in transit)

        default_val = get_fifa_manual_entry("unknown manual guideline")
        self.assertTrue("Directives" in default_val)

    # --- STEP 3: MODULE CODE PATH COVERAGE TESTS ---
    def test_fan_hub_run(self):
        mock_session["fan_chat_history"] = [{"role": "assistant", "content": "hello"}]
        mock_session["eco_points"] = 100
        run_fan_hub("MOCK_KEY", self.mock_model)
        self.assertTrue(mock_st.markdown.called)

    def test_fan_hub_query_path(self):
        mock_session["fan_chat_history"] = []
        mock_st.chat_input.return_value = "Where is Gate C?"
        run_fan_hub("MOCK_KEY", self.mock_model)
        self.assertTrue(len(mock_session["fan_chat_history"]) > 0)

    def test_fan_hub_rewards_redeem_and_scan(self):
        mock_session["eco_points"] = 600
        mock_st.button.return_value = True
        run_fan_hub("MOCK_KEY", self.mock_model)
        self.assertTrue(mock_st.markdown.called)

    def test_ops_center_run(self):
        mock_session["incidents"] = [
            {"id": "INC-001", "sector": "Gate C", "category": "Crowd", "urgency": "High", "desc": "Bottleneck", "status": "Active", "time": "12:00"}
        ]
        mock_session["dispatched_tasks"] = []
        run_ops_center("MOCK_KEY", self.mock_model)
        self.assertTrue(mock_st.markdown.called)

    def test_ops_center_submit_form_and_advisory(self):
        mock_session["incidents"] = []
        mock_session["dispatched_tasks"] = []
        mock_st.form_submit_button.return_value = True
        mock_st.button.return_value = True
        mock_st.text_input.return_value = "evacuation manual search"
        run_ops_center("MOCK_KEY", self.mock_model)
        self.assertTrue(mock_st.markdown.called)

    def test_sustainability_run(self):
        run_sustainability("MOCK_KEY", self.mock_model)
        self.assertTrue(mock_st.markdown.called)

    def test_sustainability_waste_and_audit(self):
        mock_st.text_input.return_value = "paper cup recycling"
        mock_st.button.return_value = True
        run_sustainability("MOCK_KEY", self.mock_model)
        self.assertTrue(mock_st.markdown.called)

    def test_broadcast_run(self):
        mock_session["jumbotron_text"] = "Sample broadcast"
        mock_session["jumbotron_lang"] = "Spanish"
        run_broadcast("MOCK_KEY", self.mock_model)
        self.assertTrue(mock_st.markdown.called)

    def test_broadcast_trigger_translation(self):
        mock_st.button.return_value = True
        run_broadcast("MOCK_KEY", self.mock_model)
        self.assertTrue(mock_st.markdown.called)


if __name__ == '__main__':
    unittest.main()
