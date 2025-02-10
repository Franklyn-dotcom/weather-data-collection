# 7 Steps To Create A Weather Data Collection Using Python, AWS and AWS SDK For Python

## Table of Contents

1. Cloning the repository
2. Configure AWS Credentials in the command line (CLI)
3. Create a virtual environment(venv)
4. Installing the packages and libraries
5. Configuring the environment variables
6. Create a Python File
7. Conclusion

Have you ever wondered how weather data is collected or analyzed?

In this article,  I will walk you through on creating a weather data collection using the power of AWS, Python, Matplotlib and the AWS SDK for Python (boto3). This approach allows you to create a scalable, and cost-effective weather data collection.

## Prerequisites
- AWS Account: Sign up for an [AWS](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all) account if you don’t already have one.
- AWS CLI: Install the [AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to interact with AWS services.
- IAM User Account: Create an IAM user with programmatic access and permissions to use S3.
- OpenWeather API Account
- Python3.7+
- Basic understanding of python
- Basic understanding of Git

## Step 1: Cloning the repository
You can clone the repository using the following command:
```bash
git clone https://github.com/Franklyn-dotcom/weather-data-collection.git
```
## Step 2: Configure AWS Credentials in the command line (CLI)
After installing the AWS CLI, You need to configure your AWS CLI to enable you to connect and access your account. Run the following command to connect your access account:
```bash 
aws configure
```
## Step 3: Create a virtual environment(venv)
After configuring your AWS CLI, You need to create a virtual environment(venv) for Python to enable you to manage separate package installations.
Run the following command to create a virtual environment:
```bash
  python -m venv <name-of-your-virtual-env-folder>
```
After creating your virtual environment, you need to activate your virtual environment before installing or using any packages in your virtual environment.

To activate the virtual environment on Windows(powershell). Run the following command:
```bash
.\venv\Script\Activate.ps1
```
![venv-activate](/Images/venv-activate.png)

On MacOs/Linux:
```bash
source venv/bin/activate
```

## Step 4: Installing the packages and libraries
After activating the virtual environment. Run the following command to install the packages using the `requirement.txt` file:
```bash
pip install -r requirements.txt
```
![pip-install](/Images/pip-install-requirements.png)

## Step 5: Configuring the environment variables
Create a .env file in the root directory and configure the following contents:
```bash
OPENWEATHER_API_KEY=your_api_key
AWS_BUCKET_NAME=your_bucket_name
```
## Step 6: Creating a Python file
After configuring the environment variables. Create a python file named `weather-data.py` and copy and paste the following code into the file:
```python
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
            temp = weather_data['list'][0]['main']['temp'] 
            feels_like = weather_data['list'][0]['main']['feels_like']
            humidity = weather_data['list'][0]['main']['humidity']
            description = weather_data['list'][0]['weather'][0]['description']
            
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
```
Lets's breakdown what the code is doing here: 
```python
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

        
    def create_bucket_if_not_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists")
        except:
            print(f"Creating bucket {self.bucket_name}")
        try:
            # check if default region is us-east-1 and create bucket 
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
```
This code create a class constructor named `WeatherDashboard` and stores different methods with each tasks to be executed. The `__init__` method takes an parameter `self`. `self` is a reference to the current instance of the class, and is used to access variables that belong to the class.

The `__init__` methods creates various objects that stores the `api_key` for the OpenWeather API, `bucket_name` for the s3 bucket creation. 

The `fetch_weather` method takes two parameters `self` and `city` and creates a dictionary that stores the request parameter and creates a `try....except...else` block that fetches weather data from the OpenWeather API and handle errors if any occurs.

The `create_bucket_if_not_exists` method takes the `self` parameter and creates a `try...except` block that creates the bucket if it doesn't already exist and returns the bucket object created with that bucket object name and handle errors if any occurs.

The `save_to_s3` method takes three parameters `self`, `weather_data`, and `city` and create a timestamp object that will be used as the timestamp for the bucket object created with the provided bucket object name and handle errors if any occurs. `try...except` blocks stores the bucket object created with the provided bucket object name and handle errors if any occurs.

```Python
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

    #create an empty list for conditions
    condtions = []
    # create an empty list for temperatures
    temperatures = []
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
            # Add temperatures and conditions to respective lists
            temperatures.append(temp)
            condtions.append(description)
            
        # visualize weather data
        visualize_weather_data(city, temp)
        
        # Save to S3
        success = dashboard.save_to_s3(weather_data, city)
        if success:
            print(f"Weather data for {city} saved to S3!")
        else:
            print(f"Failed to fetch weather data for {city}")
    
    # Visualize the weather data using a graphing library (matplotlib)
    def visualize_weather_data(city, temp, description):
        # Visualize the weather data using matplotlib.
        axes = plt.subplots()[1]
        # Create a bar chart
        axes.bar(city, temp, color= 'skyblue')
        axes.set_xlabel('City')
        axes.set_ylabel('Temperature (°F)')
        axes.set_title(f"Weather in {city} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Annotate each bar chart with the weather conditions
        for i, condition in enumerate(description):
            axes.text(i, temp[i], condition, ha='center', va='bottom')

        # Display the plot
        plt.show()
    
    return "Weather data collected successfully"

```
This code creates a function name `main` that stores the instance of a class in a variable name `dashboard`. The `main` function fetches the weather daa for predefined cities, saves it to an S3 bucket, print the status of the weather data and visualize the weather data using matplotlib.

The `visualize_weather_data` function creates a bar chart of the temperature for each city and annotates each bar with the weather condition.

Click here to learn more about matplotlib: (Matplotlib)[https://www.youtube.com/watch?v=UO98lJQ3QGI&list=PL-osiE80TeTvipOqomVEeZ1HRrcEvtZB_]

Run the following command to execute the application

```python 
python weather_dashboard.py
```
You should see the following output:


## Step 7: Conclusion

Congratulations! You’ve successfully built a weather data collection system using Python, AWS, and Boto3. This system fetches real-time weather data, stores it in an S3 bucket, and visualizes it using Matplotlib.