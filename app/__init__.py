
from flask import Flask
from flask_openai import OpenAI
from flask_pymongo import PyMongo
from .config import Config
import requests
import openai
import re

mongo = PyMongo()
openai_client = OpenAI()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configuração da chave de API do OpenAI
    openai.api_key = Config.OPENAI_API_KEY

    mongo.init_app(app)
    openai_client.init_app(app)
    
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app