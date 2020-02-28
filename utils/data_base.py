#libraries used for connecting to the database
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from sqlalchemy import create_engine
from utils.app import app
#migrate libraries
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

db = SQLAlchemy(app)
#migrate commands
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

#creating the table
class ImageData(db.Model):
    #column id
    id = db.Column(db.Integer,primary_key = True)
    #column name of the image
    name = db.Column(db.String(300),unique = False)
    #Pic binary data
    pic = db.Column(db.LargeBinary)

