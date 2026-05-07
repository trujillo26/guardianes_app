from flask import Flask
from config import Config
from controllers.auth_controller import auth_bp
from controllers.incidente_controller import incidente_bp
from controllers.publicacion_controller import publicacion_bp
from init_db import init_db

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth_bp)
app.register_blueprint(incidente_bp)
app.register_blueprint(publicacion_bp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
