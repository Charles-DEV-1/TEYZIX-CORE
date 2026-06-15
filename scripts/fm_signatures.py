import inspect
import importlib
m = importlib.import_module('flask_migrate')
for name in ('init','migrate','upgrade'):
    obj = getattr(m, name)
    try:
        print(name, inspect.signature(obj))
    except Exception as e:
        print(name, 'signature error', e)
