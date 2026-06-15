import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask
import app
f = Flask(app.__name__, instance_relative_config=False)
print('Flask class type:', type(Flask))
print('constructed type:', type(f))
print('repr:', repr(f))
print('import_name:', f.import_name)
print('config type:', type(f.config))
print('has get:', hasattr(f.config, 'get'))
print('config repr:', repr(f.config)[:200])
