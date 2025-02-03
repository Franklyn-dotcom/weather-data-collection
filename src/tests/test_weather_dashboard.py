import unittest
from unittest.mock import patch
from src.weather_dashboard import main

class TestWeatherDashboard(unittest.TestCase):
    @patch('builtins.input', side_effect=['yes'])  # Mock input to simulate user input
    def test_main_function(self, mock_input):
        result = main()
        expected_result = "Weather data collected successfully"
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()