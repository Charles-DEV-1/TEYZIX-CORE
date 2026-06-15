import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
except Exception:
    pass

from app import create_app
import flask_migrate as fm

app = create_app()
import traceback

print('app.extensions keys before app_context:', list(app.extensions.keys()))
with app.app_context():
    print('app.extensions keys inside app_context:', list(app.extensions.keys()))
    try:
        from app.extensions import db as db_ext
        print('imported db from app.extensions:', bool(db_ext))
    except Exception as e:
        print('import db error:', repr(e))
    try:
        fm.init(directory='migrations')
        print('init ok')
    except Exception as e:
        print('init error:', repr(e))
        traceback.print_exc()
    try:
        fm.migrate(directory='migrations', message='initial')
        print('migrate ok')
    except Exception as e:
        print('migrate error:', repr(e))
        traceback.print_exc()
    try:
        fm.upgrade(directory='migrations')
        print('upgrade ok')
    except Exception as e:
        print('upgrade error:', repr(e))
        traceback.print_exc()
