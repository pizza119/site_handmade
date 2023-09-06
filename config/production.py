from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'b\x05\x99\xb3L\xff\xef\xe4\x08\xc2V{\xe2>\xa4\x8f'