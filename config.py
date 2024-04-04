from dotenv import load_dotenv
import os
import yaml

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

db_name = os.getenv("db_name")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
database_url: str = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
# database_url: str = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
yaml_templates = 'app/text_templates.yaml'

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = database_url or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 20


class TextTemplates():
    """
    Represents text templates from yaml file.
    """
    text_templates = yaml.safe_load(yaml_templates)


def get_text_templates():
    """
    Retrieve the text_templates object that holds yaml attributes.

    Returns:
        text_templates object: The text_templates object that holds various strings and texts for app.

    """
    return TextTemplates().text_templates