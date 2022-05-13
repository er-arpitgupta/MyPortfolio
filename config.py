import os

class Config():
    SECRET_KEY = os.environ.get('SSECRET_KEY') or 'secret_string'