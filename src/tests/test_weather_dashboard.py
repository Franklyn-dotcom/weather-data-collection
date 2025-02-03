import unittest
from src.weather_dashboard import WeatherDashboard, main  

class TestWeatherDashboard(unittest.TestCase):
    def test_some_function(self):
        result =   WeatherDashboard()
        expected_result = "Weather data collected successfully"
        self.assertEqual(result, expected_result) 

if __name__ == '__main__':
    unittest.main()