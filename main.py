import requests
import json
import sqlite3
from win10toast import ToastNotifier


api_key = '53eb4cd5466d27d9c30a9ad65d93a1d9'
city = 'Tbilisi'


url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
response = requests.get(url)

if response.status_code == 200:
    print("API request successful.")

    headers = response.headers
    print("Headers:", headers)
else:
    print("API request failed.")


json_data = response.json()
with open('weather_data.json', 'w') as file:
    json.dump(json_data, file, indent=4)


temperature = json_data['main']['temp']
print("Current temperature:", temperature)


conn = sqlite3.connect('weather.db')


create_table_query = '''
CREATE TABLE IF NOT EXISTS weather (
    city TEXT,
    temperature REAL,
    humidity INTEGER,
    pressure INTEGER
);
'''
conn.execute(create_table_query)


insert_query = '''
INSERT INTO weather (city, temperature, humidity, pressure)
VALUES (?, ?, ?, ?);
'''
conn.execute(insert_query, (city, temperature, json_data['main']['humidity'], json_data['main']['pressure']))

conn.commit()
conn.close()


toaster = ToastNotifier()

notification_title = f"Weather in {city}"
notification_message = f"Temperature: {temperature}C"
