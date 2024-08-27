from flask_pymongo import PyMongo

mongo = PyMongo()

# Importa modelos
from .product import Product
from .user import User