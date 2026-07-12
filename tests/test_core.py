import sys
from unittest.mock import MagicMock

# --- STEP 1: MOCK STREAMLIT ---
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
import unittest
from modules.utils import (
    sanitize_input,
    get_routing_steps,
    get_waste_sorting_recommendation,
    get_broadcast_translation_fallback,
    get_fifa_manual_entry
)
from modules.fan_hub import run_fan_hub
from modules.ops_center import run_ops_center
from modules.sustainability import run_sustainability
from modules.broadcast import run_broadcast

class TestArenaFlowAI(unittest.TestCase):
    def setUp(self):
        self.mock_model = MagicMock()
        self.mock_response = MagicMock()
        self.mock_response.text = "Mock GenAI Response Text"
        self.mock_model.generate_content.return_value = self.mock_response
        
        # Reset session state before each test
        mock_session.clear()

    def test_mock_gemini_interaction(self):
        prompt = "Hello AI"
        response = self.mock_model.generate_content(prompt)
        self.assertEqual(response.text, "Mock GenAI Response Text")
        self.mock_model.generate_content.assert_called_once_with(prompt)

    def test_sanitize_input(self):
        self.assertEqual(sanitize_input("Hello <script>alert('XSS')</script> World"), "Hello alert(&#x27;XSS&#x27;) World")
        self.assertEqual(sanitize_input("   Lead space strip   "), "Lead space strip")
        self.assertEqual(sanitize_input(None), "")
        self.assertEqual(sanitize_input("<b>Bold</b>"), "Bold")

    def test_get_routing_steps(self):
        steps_std = get_routing_steps("Gate A", "Section 104", "Standard")
        self.assertTrue(len(steps_std) > 0)
        self.assertTrue("Gate A" in steps_std[0][1])

    def test_get_waste_sorting_recommendation(self):
        compost = get_waste_sorting_recommendation("banana peel")
        self.assertTrue("Compost" in compost)

    def test_get_broadcast_translation_fallback(self):
        spanish_shuttle = get_broadcast_translation_fallback("shuttle bus to MetLife", "Spanish")
        self.assertTrue("MetLife" in spanish_shuttle)

    def test_get_fifa_manual_entry(self):
        evac = get_fifa_manual_entry("evacuation protocol")
        self.assertTrue("Assembly" in evac)

    # --- STEP 3: RUN TESTS ---
    def test_fan_hub_run(self):
        mock_session["fan_chat_history"] = [{"role": "assistant", "content": "hello"}]
        mock_session["eco_points"] = 100
        run_fan_hub("MOCK_KEY", self.mock_model)
        self.assertTrue(mock_st.markdown.called)

    def test_ops_center_run(self):
        mock_session["incidents"] = [
            {"id": "INC-001", "sector": "Gate C", "category": "Crowd", "urgency": "High", "desc": "Bottleneck", "status": "Active", "time": "12:00"}
        ]
        mock_session["dispatched_tasks"] = []
        run_ops_center("MOCK_KEY", self.mock_model)
        self.assertTrue(mock_st.markdown.called)

    def test_sustainability_run(self):
        run_sustainability("MOCK_KEY", self.mock_model)
        self.assertTrue(mock_st.markdown.called)

    def test_broadcast_run(self):
        mock_session["jumbotron_text"] = "Sample broadcast"
        mock_session["jumbotron_lang"] = "Spanish"
        run_broadcast("MOCK_KEY", self.mock_model)
        self.assertTrue(mock_st.markdown.called)

if __name__ == '__main__':
    unittest.main()
