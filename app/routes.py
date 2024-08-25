import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request
from email_validator import validate_email
from datetime import timedelta
from datetime import datetime
from functools import wraps
from bson import ObjectId
from app.models.product import Product
from .models import User
from app.config import Config
from . import openai
from assistant import *
from flask import Flask, request, jsonify
import openai
import re
from config import Config
from assistant import PlantingAssistant





main = Blueprint('main', __name__)

# Decoradores
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        # token = token.replace('Bearer ', "")

        if not token:
            return jsonify({"error": "Invalid Token"}), 403
        
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = User.get_user_by_id(ObjectId(data['sub']))  # Obter usuário pelo ID
    
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated









# Rotas para usuários
@main.route('/users', methods=['GET'])
@token_required
def get_users(arg):
    users = User.get_all_users()
    user_list = []

    for user in users:
        user['_id'] = str(user['_id'])
        user_list.append(user)

    return jsonify({"data": user_list})

@main.route('/users/<user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    user = User.get_user_by_id(ObjectId(user_id))

    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    
    return jsonify({"error": "Usuário não encontrado"}), 404

@main.route('/users', methods=['POST'])
@token_required
def create_user():
    data = request.json

    if not data['email']:
        return jsonify({"error": 'E-mail não pode ser nulo'}), 400
    
    if not data['password']:
        return jsonify({"error": 'Senha não pode ser nula'}), 400
    
    if  not validate_email(data['email']):
        return jsonify({"error": 'E-mail inválido'}), 400
    
    if User.get_user_by_email(data['email']):
        return jsonify({"error": 'Este e-mail já está cadastrado'}), 409
    
    hashed_password = generate_password_hash(data['password'])
    data['password'] = hashed_password

    user = User.from_dict(data)
    User.create_user(user.to_dict())

    return jsonify({"message": 'Usuário criado!'}), 201

@main.route('/users/<user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    data = request.json
    user = User.from_dict(data)
    result = User.update_user(ObjectId(user_id), user.to_dict())

    if result.matched_count:
        return jsonify({"message": "Usuário atualizado!"}), 200
    
    return jsonify({"error": "Usuário não encontrado"}), 404

@main.route('/users/<user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    result = User.delete_user(ObjectId(user_id))
    if result.deleted_count:
        return jsonify({"message": "Usuário excluído!"}), 200
    
    return jsonify({"error": "Usuário não encontrado"}), 404








# Rotas para autenticação
@main.route('/login', methods=['POST'])
def login():
    data = request.json

    email = data['email']
    pwd = data['password']

    if not email:
        return jsonify({"error": 'E-mail não pode ser nulo'}), 400
    
    if not pwd:
        return jsonify({"error": 'Senha não pode ser nula'}), 400
    
    user_found = User.get_user_by_email(email)
    if not user_found:
        return jsonify({"error": 'Usuário não encontrado'}), 404
    
    hashed_password = user_found['password']

    if not check_password_hash(hashed_password, pwd):
        return jsonify({"error": 'Senha incorreta'}), 401
    

    token = jwt.encode({
        'sub': str(user_found['_id']),
        'exp': datetime.now() + timedelta(hours=24) # 24h para o token expirar
    }, Config.SECRET_KEY, algorithm='HS256')

    data = {
        "id": str(user_found['_id']),
        "name": user_found['name'],
        "email": user_found['email'],
        "token": token
    }
    
    return jsonify({"message": "Login realizado com sucesso!", "data": data}), 200











# Rota para obter todos os produtos
@main.route('/produtos', methods=['GET'])
@token_required
def obter_produtos():
    produtos = AgriculturalProduct.get_all_products()
    lista_produtos = []

    for produto in produtos:
        produto['_id'] = str(produto['_id'])
        lista_produtos.append(produto)

    return jsonify({"dados": lista_produtos})

# Rota para obter um produto específico pelo ID
@main.route('/produtos/<produto_id>', methods=['GET'])
@token_required
def obter_produto(produto_id):
    produto = AgriculturalProduct.get_product_by_id(ObjectId(produto_id))

    if produto:
        produto['_id'] = str(produto['_id'])
        return jsonify(produto)
    
    return jsonify({"erro": "Produto não encontrado"}), 404

# Rota para criar um novo produto
@main.route('/produtos', methods=['POST'])
@token_required
def criar_produto():
    dados = request.json
    novo_produto = AgriculturalProduct.from_dict(dados)
    produto_id = AgriculturalProduct.create_product(novo_produto.to_dict())

    return jsonify({"mensagem": "Produto criado com sucesso", "produto_id": str(produto_id.inserted_id)})

# Rota para atualizar um produto existente
@main.route('/produtos/<produto_id>', methods=['PUT'])
@token_required
def atualizar_produto(produto_id):
    dados = request.json
    atualizado = AgriculturalProduct.update_product(ObjectId(produto_id), dados)

    if atualizado.matched_count > 0:
        return jsonify({"mensagem": "Produto atualizado com sucesso"})
    
    return jsonify({"erro": "Produto não encontrado"}), 404

# Rota para excluir um produto
@main.route('/produtos/<produto_id>', methods=['DELETE'])
@token_required
def excluir_produto(produto_id):
    resultado = AgriculturalProduct.delete_product(ObjectId(produto_id))

    if resultado.deleted_count > 0:
        return jsonify({"mensagem": "Produto excluído com sucesso"})
    
    return jsonify({"erro": "Produto não encontrado"}), 404

# Rota para obter produtos em estoque
@main.route('/produtos/em_estoque', methods=['GET'])
@token_required
def obter_produtos_em_estoque():
    produtos = AgriculturalProduct.get_products_in_stock()
    lista_produtos = []

    for produto in produtos:
        produto['_id'] = str(produto['_id'])
        lista_produtos.append(produto)

    return jsonify({"dados": lista_produtos})









#Rota Chat GPT 
@main.route('/generate-text', methods=['POST'])
def generate_text():
    data = request.get_json()
    msg = data.get('msg', '')
    
    # Inicializar o PlantingAssistant
    planting_assistant = PlantingAssistant(api_key=app.config['WEATHER_API_KEY'])
    
    def is_weather_question(message):
        weather_keywords = ['clima', 'tempo', 'previsão', 'temperatura', 'como está o tempo', 'como está o clima']
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in weather_keywords)
    
    def extract_city_from_message(message):
        match = re.search(r'em ([A-Za-zÀ-ÖØ-öø-ÿ\s]+)', message, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        else:
            return None  # Cidade não encontrada
    
    if is_weather_question(msg):
        city = extract_city_from_message(msg)
        if city:
            weather_data = planting_assistant.get_weather(city)
            if weather_data:
                system_message = (
                    "Você é um fazendeiro profissional com conhecimento profundo sobre técnicas de plantio, "
                    "melhores práticas agrícolas, gestão de solo e clima, e otimização da produção. "
                    "Use as informações meteorológicas fornecidas para orientar o usuário adequadamente."
                )
                user_message = (
                    f"O usuário perguntou sobre o clima em {weather_data['city']}. "
                    f"As condições atuais são: {weather_data['weather']} com temperatura de {weather_data['temp']}°C. "
                    "Forneça conselhos relevantes baseados nessas informações."
                )
            else:
                system_message = (
                    "Você é um fazendeiro profissional com conhecimento profundo sobre técnicas de plantio, "
                    "melhores práticas agrícolas, gestão de solo e clima, e otimização da produção."
                )
                user_message = (
                    f"Não foi possível obter os dados meteorológicos para a cidade {city}. "
                    "Por favor, forneça orientações gerais sobre condições climáticas."
                )
        else:
            system_message = (
                "Você é um fazendeiro profissional com conhecimento profundo sobre técnicas de plantio, "
                "melhores práticas agrícolas, gestão de solo e clima, e otimização da produção."
            )
            user_message = (
                "O usuário perguntou sobre o clima, mas não especificou uma localização válida. "
                "Peça ao usuário para fornecer o nome da cidade."
            )
    else:
        system_message = (
            "Você é um fazendeiro profissional com conhecimento profundo sobre técnicas de plantio, "
            "melhores práticas agrícolas, gestão de solo e clima, e otimização da produção."
        )
        user_message = msg
    
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        response_text = completion.choices[0].message['content']
        return jsonify({'message': response_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



    






        
'''

'''

# Rotas para o assistente
# @main.route('/weather', methods=['GET'])
# def weather():
#     city = request.args.get('city')
#     if not city:
#         flash('Por favor, insira o nome da cidade.')
#         return redirect(url_for('home'))
    
#     weather_data = assistant.get_weather(city)
#     if "error" in weather_data:
#         flash(weather_data["error"])
#         return redirect(url_for('home'))
    
#     planting_advice = assistant.can_plant(weather_data["temp"], weather_data["weather"])
#     return render_template('weather.html', weather_data=weather_data, planting_advice=planting_advice)

# @main.route('/check_ph', methods=['POST'])
# def check_ph():
#     try:
#         ph_level = float(request.form.get('ph'))
#     except ValueError:
#         flash('Por favor, insira um valor numérico válido para o pH.')
#         return redirect(url_for('home'))
    
#     advice = assistant.check_ph(ph_level)
#     return render_template('ph.html', ph_level=ph_level, advice=advice)


