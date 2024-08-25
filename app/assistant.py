from flask import Flask, request, jsonify
import openai
import requests
from config import Config

app = Flask(__name__)

# Configuração da chave de API do OpenAI
openai.api_key = Config.OPENAI_API_KEY

class PlantingAssistant:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        response = requests.get(url)
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

# Rota do ChatGPT
@app.route('/generate-text', methods=['POST'])
def generate_text():
    data = request.json
    msg = data['msg']

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é muito legal!"},
            {"role": "user", "content": msg}
        ]
    )

    response_text = completion.choices[0].message['content']
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
