import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'feynman.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "y_never_know_my_secret_key_hahaha"

# print(SQLALCHEMY_DATABASE_URI)
