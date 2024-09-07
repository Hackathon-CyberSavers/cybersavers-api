import jwt
import re
import google.generativeai as genai
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request
from email_validator import validate_email
from datetime import timedelta
from datetime import datetime
from functools import wraps
from bson import ObjectId
from app.models.product import Product
from .models import User
from .config import Config
from .assistant import PlantingAssistant


main = Blueprint('main', __name__)

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="You are an assistant who helps farmers with their general questions about their farms, such as: questions about pH and planting tips. Your name is Tanica"
)


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
    produtos = Product.get_all_products()
    lista_produtos = []

    for produto in produtos:
        produto['_id'] = str(produto['_id'])
        lista_produtos.append(produto)

    return jsonify({"dados": lista_produtos})

# Rota para obter um produto específico pelo ID
@main.route('/produtos/<produto_id>', methods=['GET'])
@token_required
def obter_produto(produto_id):
    produto = Product.get_product_by_id(ObjectId(produto_id))

    if produto:
        produto['_id'] = str(produto['_id'])
        return jsonify(produto)
    
    return jsonify({"erro": "Produto não encontrado"}), 404

# Rota para criar um novo produto
@main.route('/produtos', methods=['POST'])
@token_required
def criar_produto():
    dados = request.json
    novo_produto = Product.from_dict(dados)
    produto_id = Product.create_product(novo_produto.to_dict())

    return jsonify({"mensagem": "Produto criado com sucesso", "produto_id": str(produto_id.inserted_id)})

# Rota para atualizar um produto existente
@main.route('/produtos/<produto_id>', methods=['PUT'])
@token_required
def atualizar_produto(produto_id):
    dados = request.json
    atualizado = Product.update_product(ObjectId(produto_id), dados)

    if atualizado.matched_count > 0:
        return jsonify({"mensagem": "Produto atualizado com sucesso"})
    
    return jsonify({"erro": "Produto não encontrado"}), 404

# Rota para excluir um produto
@main.route('/produtos/<produto_id>', methods=['DELETE'])
@token_required
def excluir_produto(produto_id):
    resultado = Product.delete_product(ObjectId(produto_id))

    if resultado.deleted_count > 0:
        return jsonify({"mensagem": "Produto excluído com sucesso"})
    
    return jsonify({"erro": "Produto não encontrado"}), 404

# Rota para obter produtos em estoque
@main.route('/produtos/em_estoque', methods=['GET'])
@token_required
def obter_produtos_em_estoque():
    produtos = Product.get_products_in_stock()
    lista_produtos = []

    for produto in produtos:
        produto['_id'] = str(produto['_id'])
        lista_produtos.append(produto)

    return jsonify({"dados": lista_produtos})








#Rota Chat GPT 
@main.route('/generate-text', methods=['POST'])
def generate_text():
    data = request.json
    msg = data["msg"]
    print (data,msg)
    
    # Inicializar o PlantingAssistant
    planting_assistant = PlantingAssistant()
    
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
        completion =model.generate_content(msg)
        
        return jsonify({'message': completion.text, "data": completion}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/llm/text', methods=['POST'])
def generate_text_2():
    data = request.json
    msg = data["msg"]
    
    response = model.generate_content(msg).to_dict()
    
    return jsonify({'message': response['candidates'][0]['content']['parts'][0]['text']}), 200
