from flask import Blueprint, render_template, request, flash, redirect, url_for, g, current_app
from .weather_service import WeatherService


bp = Blueprint('main', __name__)
weather_service = WeatherService()

@bp.before_app_request
def load_city():
    g.city = None
    city = request.cookies.get('city')
    if city:
        g.city = {"name": city}

@bp.route("/", methods=["GET", "POST"])
def index():
    if g.city:
        # Si ya hay una ciudad guardada, redirigir a la página del clima
        return redirect(url_for("main.weather", city=g.city['name']))
    return render_template("index.html")

@bp.route("/search", methods=["POST"])
def search():
    city = request.form.get("city")
    if not city:
        flash("Please enter a city name.")
        return redirect(url_for("index"))
    
    return redirect(url_for("main.weather", city=city))

@bp.route('/weather/<city>')
def weather(city):
    current_weather, forecast = weather_service.get_weather_data(city)

    if current_weather is None:
        # Si no se encuentra la ciudad, redirigir a la página de inicio
        flash(f"No se encontró la ciudad: {city}")
        return redirect(url_for('main.index'))
    
    g.city = {'name': city}
    
    response = current_app.make_response(
        render_template('weather.html', weather=current_weather, forecast=forecast)
    )
    response.set_cookie('city', city, max_age=60*60*24*30)  # 30 días
    return response

@bp.route('/clear')
def clear():
    response = redirect(url_for('main.index'))
    response.delete_cookie('city')
    return response
