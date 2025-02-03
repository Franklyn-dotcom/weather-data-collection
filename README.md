# Weather Data Collection System
A python Application that fetches real-time weather data from OpenWeather API, collects user input to add another city to the list of cities and automate it using a streamline pipeline.

## Features
- Fetches current weather data including temperature, humidity, and weather description for selected cities.
- Collects user input to add another city to the list of cities.
- Creates an S3 bucket containing weather data for selected cities and stores them in a json format.
- A streamline pipeline used for automating the application and testing the application. 

## Prerequisites
- AWS Account
- AWS CLI
- IAM User Account for access keys and secret keys
- OpenWeather API Account
- Basic understanding of python

## How to Run:
### 1. Clone the repository:
```bash
git clone https://github.com/Franklyn-dotcom/weather-data-collection.git
```

### 2. Configure AWS Credential in the CLI:
After installing the AWS CLI, You need to configure your AWS CLI to enable you to connect and access your account. Run the following command to connect your aws account:
```bash
aws configure
```

### 3. Create a virtual environment(venv)
After configuring your AWS CLI, You need to create a virtual environment(venv) for Python to enable you to manage separate package installations.
Run the following command to create a virtual environment:
```bash
  python -m venv <name-of-your-virtual-env-folder>
```


To activate the virtual environment in powershell. Run the following command:
```bash
.\venv\Script\Activate.ps1
```
![venv-activate](/Images/venv-activate.png)


### 4. Install the dependencies
Run the following command to install the dependencies using the `requirement.txt file`:
```bash
pip install -r requirements.txt
```
![pip-install](/Images/pip-install-requirements.png)

### 5. Configure environment variables (.env):
Create a .env file in the root directory with the following content:
```bash
OPENWEATHER_API_KEY=your_api_key
AWS_BUCKET_NAME=your_bucket_name
```
### 6. Run the application:
To run the application, run the following command:
```bash
python src/weather_dashboard.py
```
![run-application](/Images/running-code-successfully.png)
![dashboard-script](/Images/dashboard-s3.png)
![dashboard-script](/Images/dashboard-s3-object.png)
![dashboard-script](/Images/dashboard-s3-object-upload.png)


## Further Enhancements
As an additional (non-challenge) feature, I created a user input to add another city and a streamline pipeline with a push event that runs a test on the application and run the application itself.

![automate-script](/Images/automate-success.png)
