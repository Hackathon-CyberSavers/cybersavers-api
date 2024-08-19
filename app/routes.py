import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request
from email_validator import validate_email
from datetime import timedelta
from datetime import datetime
from functools import wraps
from bson import ObjectId

from .models import User
from app.config import Config


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
def get_user(user_id):
    user = User.get_user_by_id(ObjectId(user_id))

    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    
    return jsonify({"error": "Usuário não encontrado"}), 404

@main.route('/users', methods=['POST'])
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
def update_user(user_id):
    data = request.json
    user = User.from_dict(data)
    result = User.update_user(ObjectId(user_id), user.to_dict())

    if result.matched_count:
        return jsonify({"message": "Usuário atualizado!"}), 200
    
    return jsonify({"error": "Usuário não encontrado"}), 404

@main.route('/users/<user_id>', methods=['DELETE'])
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


