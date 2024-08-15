from app import create_app
from app.config import Config

dbg = True if Config.DEBUG == '1' else False

app = create_app()

if __name__ == '__main__':
    app.run(debug=dbg)
