import sqlite3
from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from auth import auth_bp
from routes.upload import upload_bp
from routes.stats import stats_bp
from routes.get_data import get_data_bp
from routes.query_data import query_data_bp  # ✅ Import new query route
from db import get_db_connection, init_db  # ✅ Import DB functions

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

# Ensure persistent SQLite database
init_db()  # ✅ Ensure metadata table is created

# Register Blueprints (routes)
app.register_blueprint(auth_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(get_data_bp)
app.register_blueprint(query_data_bp)  # ✅ Register new query route

if __name__ == "__main__":
    app.run(debug=True)
