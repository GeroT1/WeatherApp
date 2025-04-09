import requests
from datetime import datetime
from .config import Config

class WeatherService:
    def __init__(self):
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.base_url_forecast = "http://api.openweathermap.org/data/2.5/forecast"
        self.units = "metric"
        self.lang = "en"

    def get_weather_data(self, city):
        try:
            current_response = requests.get(
                f"{self.base_url}?q={city}&appid={self.api_key}&units={self.units}&lang={self.lang}"
                
            )

            if current_response.status_code == 404:
                print("City not found")
                return None, None

            if current_response.status_code != 200:
                print(f"Error fetching weather data: {current_response.status_code}")
                return None, None
            
            
            
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
                f"{self.base_url_forecast}?q={city}&appid={self.api_key}&units={self.units}&lang={self.lang}&cnt=40"
            )

            if forecast_response.status_code != 200:
                print(f"Error fetching forecast data: {forecast_response.status_code}")
                return current, []
            
            forecast_data = forecast_response.json()

            daily_data = {}

            for item in forecast_data["list"]:
                dt = datetime.fromtimestamp(item["dt"])
                day_str = dt.strftime("%Y-%m-%d")

                if day_str not in daily_data:
                    daily_data[day_str] = {
                        "date": dt.strftime("%a %d"),
                        "temp_min": 9999,
                        "temp_max": -9999,
                        "icon": None,
                        "icon_count": {}
                    }

                daily_data[day_str]["temp_min"] = min(daily_data[day_str]["temp_min"], item["main"]["temp_min"])
                daily_data[day_str]["temp_max"] = max(daily_data[day_str]["temp_max"], item["main"]["temp_max"])

                icon = item["weather"][0]["icon"]
                daily_data[day_str]["icon_count"][icon] = daily_data[day_str]["icon_count"].get(icon, 0) + 1

            forecast = []
            for day_str in sorted(daily_data.keys())[:5]:
                day_info = daily_data[day_str]
                most_common_icon = max(day_info["icon_count"].items(), key=lambda x: x[1])[0]

                forecast.append({
                    "date": day_info["date"],
                    "temp_min": round(day_info["temp_min"]),
                    "temp_max": round(day_info["temp_max"]),
                    "icon_url": f"http://openweathermap.org/img/wn/{most_common_icon}.png"
                })

            return current, forecast


        except Exception as e:
            print(f"Error fetching weather data:{e}")
            return None, None