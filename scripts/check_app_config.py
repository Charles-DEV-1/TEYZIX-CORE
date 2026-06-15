import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from flask import Flask as FlaskClass
print('FlaskClass:', FlaskClass)
print('FlaskClass type:', type(FlaskClass))
app = create_app()
print('type(app):', type(app))
print('type(app.config):', type(app.config))
print('has get:', hasattr(app.config, 'get'))
print('app.config class:', app.config.__class__)
print('config keys sample:', list(app.config.keys())[:10])
