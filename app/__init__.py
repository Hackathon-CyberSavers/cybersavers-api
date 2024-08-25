from flask import Flask
from flask_pymongo import PyMongo
from .config import Config
from flask_openai import OpenAI

mongo = PyMongo()
openai = OpenAI()

def create_app():
    app = Flask(__name__)
    
    # Configurações de API
    app.config.from_object(Config)
    
    # Inicializa o MongoDB e o OpenAI com as configurações do app
    mongo.init_app(app)
    openai.init_app(app)

    # Inicializa o PlantingAssistant com a chave da API de clima
    from .assistant import PlantingAssistant
    assistant = PlantingAssistant(api_key=app.config['WEATHER_API_KEY'])
    
    # Registra as rotas do blueprint
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Armazena o assistant como uma variável global ou anexa ao app para uso posterior
    app.planting_assistant = assistant
    
    return app
