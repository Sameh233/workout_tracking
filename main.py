import requests
import json
from datetime import datetime


with open('credentials.json', mode= 'r') as file :
    data = json.load(file)
    
headers = {
    'Content-Type': 'application/json',
    'x-app-id': data['app_id'] ,
    'x-app-key': data['api_key']
  }

activity = {
    'query': input('Tell me which exercises you did: ')
  }

response = requests.post(url = 'https://trackapi.nutritionix.com/v2/natural/exercise', headers= headers, json = activity)
response.raise_for_status()

nutritionix_data = response.json()


# formatting the date and time 

date = datetime.now().strftime('%d/%m/%Y')
time = datetime.now().strftime('%H:%M:%S')

       
# connecting with the spreadsheet

sheety_headers = {
    'Authorization' : data['sheety_token']
  }

for activity in nutritionix_data['exercises'] :
    exercise = activity['name'].title()
    duration = activity['duration_min']
    calories = activity['nf_calories']
    
    sheety_body = {
    'workout' : {
      'date': date,
      'time': time,
      'exercise': exercise,
      'duration': duration, 
      'calories': calories
    },

    }
    
    sheety_api_response = requests.post(url = data['sheety_api_url'], headers= sheety_headers, json = sheety_body)
    sheety_api_response.raise_for_status()

    json_response = sheety_api_response.json()


