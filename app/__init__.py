import os.path

if os.path.exists('app/private_config.py'):
    import app.private_config as config
else:
    import app.config