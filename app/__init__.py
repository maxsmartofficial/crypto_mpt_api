from flask import Flask
from flask_cors import CORS

from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "filesystem",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 86400,
    "CACHE_DIR": "./cache/"
}
app = Flask(__name__)
CORS(app)

app.config.from_mapping(config)
cache = Cache(app)

from app import routes