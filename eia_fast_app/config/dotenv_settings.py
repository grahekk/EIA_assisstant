from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Define settings using os.getenv()
# DATABASE_URL = os.getenv("DATABASE_URL")
# SECRET_KEY = os.getenv("SECRET_KEY")

db_name = os.getenv("db_name")
username = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
