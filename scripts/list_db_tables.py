import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
url = os.getenv('DATABASE_URL')
print('DATABASE_URL =', url)
engine = create_engine(url)
inspector = inspect(engine)
print('tables =', inspector.get_table_names())
print('schemas =', inspector.get_schema_names())
