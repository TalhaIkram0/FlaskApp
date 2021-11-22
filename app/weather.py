import requests
from flask import Blueprint, session

from .constants import weather_api_url, weather_api_key

bp = Blueprint('weather', __name__, url_prefix='/weather')

@bp.route('/current/<city>', methods=('GET',))
def current_weather(city):
    if 'username' in session:
        query_endpoint = f"&q={city}&aqi=no"
        query = f"{weather_api_url}{weather_api_key}{query_endpoint}"

        response = requests.get(query)

        weather_data = response.json()

        return weather_data
    return "You need to login to view this page!"
