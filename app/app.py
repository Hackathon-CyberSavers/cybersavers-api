from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from assistant import PlantingAssistant
from commodity_price import 
from models import db, User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

api_key = "96b7d7524b7a7571fe675adc64ac39a0"
assistant = PlantingAssistant(api_key)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login inválido. Verifique suas credenciais.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/weather', methods=['GET'])
@login_required
def weather():
    city = request.args.get('city')
    if not city:
        flash('Por favor, insira o nome da cidade.')
        return redirect(url_for('home'))
    
    weather_data = assistant.get_weather(city)
    if "error" in weather_data:
        flash(weather_data["error"])
        return redirect(url_for('home'))
    
    planting_advice = assistant.can_plant(weather_data["temp"], weather_data["weather"])
    return render_template('weather.html', weather_data=weather_data, planting_advice=planting_advice)

@app.route('/check_ph', methods=['POST'])
@login_required
def check_ph():
    try:
        ph_level = float(request.form.get('ph'))
    except ValueError:
        flash('Por favor, insira um valor numérico válido para o pH.')
        return redirect(url_for('home'))
    
    advice = assistant.check_ph(ph_level)
    return render_template('ph.html', ph_level=ph_level, advice=advice)

# Endpoint para obter o preço da commodity em tempo real
@app.route('/api/commodity-price', methods=['GET'])
@login_required  # Protege a rota com autenticação
def get_commodity_price_endpoint(name):
    """
    Endpoint para obter o valor de uma commodity em tempo real, incluindo conversão para BRL.

    Args:
    name (str): Nome da commodity a ser pesquisada.

    Returns:
    json: Retorna o preço atual da commodity em USD, BRL, a taxa de câmbio e a data.
    """
    commodity_data = get_commodity_price(name)

    if "error" in commodity_data:
        return jsonify(commodity_data), 404  # Retorna erro 404 se não encontrar os dados

    return jsonify(commodity_data), 200  # Retorna os dados da commodity em formato JSON
