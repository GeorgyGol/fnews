from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap, __version__
from flask_sqlalchemy import SQLAlchemy
import hashlib

from pathlib import Path
import os

appFL = Flask(__name__)
bootstrap = Bootstrap(appFL)

# print('flask version', __version__)
# print('flask application', appFL.name)

# from app.database.config import user, password, server, database_name, wtf_seckey

user = os.environ['DBUSER']
password = os.environ['DBPASS']
server = os.environ['DBSERVER']
database_name = os.environ['DATABASE']
wtf_seckey = bytearray(os.environ['WTF_SECRET'].encode())


bot_token = os.environ['BOT_TOKEN']
channel_id = os.environ['CHANNAL_ID']

appFL.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pymssql://{user}:{password}@{server}/{database_name}'

appFL.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# appFL..config.from_object('config')

appFL.config['SECRET_KEY'] = hashlib.sha1(wtf_seckey).hexdigest()

db_main = SQLAlchemy(appFL)