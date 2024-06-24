import requests
from twilio.rest import Client
from datetime import datetime

# Twilio Account SID and Auth Token
account_sid = 'YOUR_TWILIO_SID'
auth_token = 'YOUR_TWILIO_AUTH_TOKEN'

# Twilio phone number (Sender number)
twilio_phone_number = '+YOUR_TWILIO_NUMBER'

# Recipient's mobile number (Your mobile number)
recipient_phone_number = '+YOUR_OWN_NUMBER'  # Replace with your mobile number

# OpenWeatherMap API key
api_key = 'YOUR_TWILIO_API_KEY'

# Flag to track whether SMS has been sent
sms_sent = False


def fetch_weather(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            message = f"Weather in {city}:\n" \
                      f"Description: {weather_description}\n" \
                      f"Temperature: {temperature}°C\n" \
                      f"Humidity: {humidity}%\n" \
                      f"Wind Speed: {wind_speed} m/s"

            return message
        else:
            return f"Failed to fetch weather data for {city}: {data['message']}"

    except Exception as e:
        return f"Error fetching weather data for {city}: {str(e)}"


def send_sms(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=recipient_phone_number
    )
    print(f"SMS sent successfully to {recipient_phone_number}")


def main():
    global sms_sent  # Declare sms_sent as global

    # List of cities to fetch weather data for
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad']

    for city in cities:
        # Fetch weather information for each city
        weather_message = fetch_weather(city)

        # Send SMS with weather information (only if not already sent)
        if weather_message and not sms_sent:
            send_sms(weather_message)
            sms_sent = True  # Set flag to True after sending first SMS
        elif sms_sent:
            print("SMS already sent. Stopping further SMS.")

    print("Weather SMS sent for all cities.")


if __name__ == '__main__':
    main()
