from flask import Flask, request, jsonify
from .config import Config

class PlantingAssistant:
    def __init__(self):
        self.api_key = Config.WEATHER_API_KEY

    def get_weather(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        response = request.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            return {
                "city": city,
                "weather": weather,
                "temp": temp
            }
        else:
            return None

    def can_plant(self, temp, weather):
        if temp < 10 or temp > 30:
            return "A temperatura não está ideal para o plantio, proteja sua plantação."
        elif 'chuva' in weather.lower():
            return "Você não precisa regar sua plantação, hoje irá chover."
        else:
            return "Boa condição para plantar."

    def check_ph(self, ph_level):
        if ph_level < 6.0:
            return (
                "O pH está baixo. Considere adicionar materiais naturais como calcário agrícola, "
                "cinzas de madeira ou conchas moídas para aumentar o pH."
            )
        elif ph_level > 7.0:
            return (
                "O pH está alto. Considere adicionar matéria orgânica como composto de folhas, agulhas de pinheiro, "
                "turfa ou borra de café para diminuir o pH."
            )
        else:
            return "O pH está adequado."


