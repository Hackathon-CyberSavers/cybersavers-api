# Nesse arquivo incializamos as bibliotecas instaladas

from flask import Flask
from flask_openai import OpenAI
from flask_pymongo import PyMongo
from .config import Config

mongo = PyMongo()
openai = OpenAI()

def create_app():
    app = Flask(__name__)
    app.config['OPENAI_API_KEY'] = "sk-svcacct-Rl7jaI6T2sEFxEdluXjtLm05ahX4FJK9v_aY9SuOmFcVDwFX8T3BlbkFJTakq1bC9G-LyhltzOsLrMx_9nuM2DCnBwyrkfJl4bixJsopDwA"
    app.config.from_object(Config)
    
    mongo.init_app(app)
    openai.init_app(app)
    
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
