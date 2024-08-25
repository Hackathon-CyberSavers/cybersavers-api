import yfinance as yf # Para informar o preço da commodity
import requests  # Importa requests para fazer requisições HTTP


def get_commodity_price(commodity_name):
    """
    Obtém o preço atual de uma commodity específica usando o yfinance e converte para BRL.

    Args:
    commodity_name (str): Nome da commodity (e.g., "Soja", "Milho").

    Returns:
    dict: Dicionário contendo o preço atual em USD, o preço convertido em BRL e a data.
    """

    def get_usd_to_brl_exchange_rate():
        """
        Obtém a taxa de câmbio USD para BRL em tempo real usando uma API pública.

        Returns:
        float: A taxa de câmbio de USD para BRL.
        """
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url)
        data = response.json()
        return data['rates']['BRL']

    # Dicionário que mapeia os nomes das commodities para seus símbolos de futuros na bolsa.
    brazilian_commodities = {
        "Soja": "ZS=F",
        "Milho": "ZC=F",
        "Café": "KC=F",
        "Algodão": "CT=F",
        "Açúcar": "SB=F"
    }

    # Obter o símbolo da commodity com base no nome fornecido.
    ticker = brazilian_commodities.get(commodity_name.capitalize())

    if not ticker:
        return {"error": "Commodity not found"}  # Retorna erro se a commodity não for encontrada.

    # Obter dados históricos da commodity usando yfinance.
    data = yf.Ticker(ticker)
    history = data.history(period="1d")  # Obtém os dados do último dia.

    if history.empty:
        return {"error": "Data not available"}  # Retorna erro se não houver dados disponíveis.

    # Obtém o último preço de fechamento e a data correspondente.
    last_price_usd = history['Close'].iloc[-1]  # Último preço de fechamento
    last_date = history.index[-1].strftime("%Y-%m-%d %H:%M:%S")  # Formata a data do último preço

    # Obter a taxa de câmbio de USD para BRL
    exchange_rate = get_usd_to_brl_exchange_rate()

    # Converter o preço de USD para BRL
    last_price_brl = last_price_usd * exchange_rate

    # Retorna um dicionário com os dados da commodity em USD e BRL.
    return {
        "name": commodity_name,
        "price_usd": round(last_price_usd, 2),
        "price_brl": round(last_price_brl, 2),
        "exchange_rate": round(exchange_rate, 2),
        "date": last_date
    }