import requests
from datetime import datetime
from config import Config

class WeatherService:
    def __init__(self):
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.units = "metric"
        self.lang = "es"

    def get_current_weather(self, city):
 
        try:
            
            current_response = requests.get(
                f"{self.base_url}?q={city}&appid={self.api_key}&units=metric&lang=es"
            )

            if current_response.status_code != 200:
                return None
            
            current_data = current_response.json()

            current = {
                "temperature": round(current_data["main"]["temp"]),
                "description": current_data["weather"][0]["description"].capitalize(),
                "humidity": current_data["main"]["humidity"],
                "wind_speed": round(current_data["wind"]["speed"] * 3.6, 1 ),
                "icon_url": f"http://openweathermap.org/img/wn/{current_data['weather'][0]['icon']}@2x.png",
                "city_name": current_data["name"],
                "country": current_data["sys"].get("country", "")
            }

            forecast_response = requests.get(
                f"{self.base_url}forecast?q=¨{city}&appid={self.api_key}&units=metric&lang=es&cnt=40"
            )

            if forecast_response.status_code != 200:
                return current, []
            
            forecast_data = forecast_response.json()

            forecast = []
            days_added = set()

            for item in forecast_data["list"]:
                dt = datetime.fromtimestamp(item["dt"])
                day_str = dt.strftime("%Y-%m-%d")

                if day_str not in days_added and dt.hour in [11, 12, 13, 14]:
                    days_added.add(day_str)
                    forecast.append({
                        "date": dt.strftime("%a %d"),
                        "temp_min": round(item["main"]["temp_min"]),
                        "temp_max": round(item["main"]["temp_max"]),
                        "icon_url": f"http://openweathermap.org/img/wn/{item['weather'][0]['icon']}.png"
                    })

                    if len(forecast) >= 5:
                        break

            return current, forecast

        except Exception as e:
            print(f"Error fetching weather data:{e}")
            return None