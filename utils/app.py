
from flask import Flask

UPLOAD_FOLDER = 'Uploads'
app = Flask(__name__)

'''
Path configuration
'''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

'''
DataBase configurations
'''

#password of the account.
password = "Kittu@201995"
DATABASE_URI = 'postgres+psycopg2://rohanvarma:'+password+'@localhost:5432/flask_test'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
