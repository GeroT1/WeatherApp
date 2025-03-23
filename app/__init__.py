from flask import Flask, render_template, request, redirect, url_for
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        '''if city:
            weather_data = get_weather(city, app.config["OPENWEATHER_API_KEY"])
        else:
            return redirect(url_for("index"))
        '''
    return render_template("index.html", weather = weather_data)
