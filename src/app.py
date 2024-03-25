import os
import redis

from dotenv import load_dotenv

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URI", "sqlite:///notes.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Initialize Flask Migrate
migrate = Migrate(app, db)

# Initialize Redis connection
redis_host = os.environ.get("REDIS_HOST")
redis_port = os.environ.get("REDIS_PORT")
redis_password = os.environ.get("REDIS_PASSWORD", "")
redis_db = os.environ.get("REDIS_DB")
redis_connection = redis.Redis(
    host=redis_host, port=redis_port, password=redis_password, db=redis_db
)

from .views import notes_bp

app.register_blueprint(notes_bp, url_prefix="/notes")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
