from flask import Flask
from config import Config, get_text_templates
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
config = app.config
text_templates = get_text_templates()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login' # ako korisnik nije ulogiran, ovdje ga fwd

from app import routes, models
with app.app_context():
    db.create_all()
