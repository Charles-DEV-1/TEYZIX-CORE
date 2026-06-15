import importlib
m = importlib.import_module('flask_migrate')
print('\n'.join([n for n in dir(m) if not n.startswith('_')]))
