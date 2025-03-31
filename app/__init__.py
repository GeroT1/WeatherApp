from flask import Flask, render_template, request, redirect, url_for, g
from config import Config
from weather import WeatherService

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

weather_service = WeatherService()

@app.before_request
def load_city():
    g.city = None
    city = request.cookies.get('city')
    if city:
        g.city = {"name": city}

@app.route("/", methods=["GET", "POST"])
def index():
    if g.city:
        return redirect(url_for("weather", city=g.city['name']))
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)