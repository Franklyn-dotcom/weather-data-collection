import os
import json
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.apiKey = os.getenv('WEATHER_FORECAST_API_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.s3_client = boto3.client('s3')


    def fetch_weather(self, city):
        """Fetch weather data from OpenWeather API"""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }
        
        # Fetch weather data from API and handle errors if any occur
        try:
            response = requests.get(base_url, params=params)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
        else:
            response.raise_for_status()
            return response.json()

    # create a function that fetch weather forecast data from weatherapi 
    def fetch_weather_forecast(self, city):
        """Fetch weather forecast data from WeatherAPI"""
        base_url = "http://api.weatherapi.com/v1/forecast.json"
        params = {
            "key": self.apiKey,
            "q": city,
            "days": 3
        }

        # Fetch weather forecast data from API and handle errors if any occur
        try:
            response = requests.get(base_url, params=params)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather forecast data: {e}")
            return None
        else:
            response.raise_for_status()
            return response.json()
        
    def create_bucket_if_not_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists")
        except:
            print(f"Creating bucket {self.bucket_name}")
        try:
            # Simpler creation for eu-north-1 region
            if os.getenv('AWS_DEFAULT_REGION') == 'us-east-1':
                self.s3_client.create_bucket(Bucket=self.bucket_name)
                print(f"Successfully created bucket {self.bucket_name}")
            else:
                self.s3_client.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': 'eu-north-1'
                    }
                )
                print(f"Successfully created bucket {self.bucket_name}")

        except Exception as e:
            print(f"Error creating bucket: {e}")


    def save_to_s3(self, weather_data, city):
        """Save weather data to S3 bucket"""
        if not weather_data:
            return False
            
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/{city}-{timestamp}.json"
        
        
        try:
            """put weather data into S3 bucket"""
            weather_data['timestamp'] = timestamp
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(weather_data),
                ContentType='application/json'
            )
            print(f"Successfully saved data for {city} to S3")
            return True
        except Exception as e:
            print(f"Error saving to S3: {e}")
            return False

def main():
    dashboard = WeatherDashboard()
    
    # Create bucket if needed
    dashboard.create_bucket_if_not_exists()
    
    cities = ["Philadelphia", "Seattle", "New York"]
    
    
    while True:
        # create an input that prompt the user if he will like to add another cities and if yes, add the city to the cities list and if no, continue with the existing cities list
        add_more = input(f"Will you like to add another city to the list? (yes/no): ").lower()
        if add_more == "yes":
            city = input("Enter city name: ")
            cities.append(city)
            break
        elif add_more == "no":
            break
        else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    for city in cities:

        print(f"\nFetching weather for {city}...")

        # create a variable to hold the weather data for the city and print the temperature, feels like, humidity and description
        weather_data = dashboard.fetch_weather(city)
        if weather_data:
            temp = weather_data['main']['temp'] 
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            
            print(f"Temperature: {temp}°F")
            print(f"Feels like: {feels_like}°F")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")

        
        # Save to S3
        success = dashboard.save_to_s3(weather_data, city)
        if success:
            print(f"Weather data for {city} saved to S3!")
        else:
            print(f"Failed to fetch weather data for {city}")
    
    return "Weather data collected successfully"
    


if __name__ == "__main__":
    main()