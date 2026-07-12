import unittest
from unittest.mock import MagicMock
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.utils import (
    sanitize_input,
    get_routing_steps,
    get_waste_sorting_recommendation,
    get_broadcast_translation_fallback
)

class TestArenaFlowAI(unittest.TestCase):
    def setUp(self):
        # Create a mock GenAI model
        self.mock_model = MagicMock()
        self.mock_response = MagicMock()
        self.mock_response.text = "Mock GenAI Response Text"
        self.mock_model.generate_content.return_value = self.mock_response

    def test_mock_gemini_interaction(self):
        # Test direct mock GenAI response generation
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

        steps_acc = get_routing_steps("Gate B", "Section 108", "Accessible")
        self.assertTrue(len(steps_acc) > 0)
        self.assertTrue("Elevator" in steps_acc[1][1] or "tactile" in steps_acc[2][1])

    def test_get_waste_sorting_recommendation(self):
        compost = get_waste_sorting_recommendation("banana peel")
        self.assertTrue("Compost" in compost)

        recycle = get_waste_sorting_recommendation("plastic tray")
        self.assertTrue("Recycling" in recycle)

        landfill = get_waste_sorting_recommendation("greasy foil")
        self.assertTrue("Landfill" in landfill)

    def test_get_broadcast_translation_fallback(self):
        spanish_shuttle = get_broadcast_translation_fallback("shuttle bus to MetLife", "Spanish")
        self.assertTrue("MetLife" in spanish_shuttle)
        self.assertTrue("autobuses" in spanish_shuttle)

if __name__ == '__main__':
    unittest.main()
