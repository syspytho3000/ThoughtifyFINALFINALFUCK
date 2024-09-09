from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("Database connection successful")
except Exception as e:
    print(f"Error connecting to the database: {e}")
