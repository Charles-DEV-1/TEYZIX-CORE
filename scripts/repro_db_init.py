import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask
from app.extensions import db, migrate
from app.config import DevelopmentConfig

print('Flask type:', type(Flask))
a = Flask(__name__, instance_relative_config=False)
print('app type before config:', type(a))
print('a.config type before config:', type(a.config), hasattr(a.config, 'get'))
a.config.from_object(DevelopmentConfig)
print('a.config type after config:', type(a.config), hasattr(a.config, 'get'))
try:
    import app.models
    print('import app.models succeeded')
except Exception as e:
    print('import app.models failed', e)
print('a.config type after import models:', type(a.config), hasattr(a.config, 'get'))
try:
    db.init_app(a)
    print('db.init_app succeeded')
except Exception as e:
    print('db.init_app failed', e)
print('a.config type after db.init_app:', type(a.config), hasattr(a.config, 'get'))
try:
    migrate.init_app(a, db)
    print('migrate.init_app succeeded')
except Exception as e:
    print('migrate.init_app failed', e)
print('a.config type after migrate.init_app:', type(a.config), hasattr(a.config, 'get'))
