from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap, __version__
from flask_sqlalchemy import SQLAlchemy
import hashlib
import re
from pathlib import Path
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)

# print('flask version', __version__)
# print('flask application: ', app.name)

# from app.database.config import user, password, server, database_name, wtf_seckey

user = os.environ['DBUSER']
password = os.environ['DBPASS']
server = os.environ['DBSERVER']
database_name = os.environ['DATABASE']
wtf_seckey = bytearray(os.environ['WTF_SECRET'].encode())
bot_token = os.environ['BOT_TOKEN']
channel_id = os.environ['CHANNAL_ID']

# def print_env():
#     print(f'{user=}')
#     print(f'{password=}')
#     print(f'{server=}')
#     print(f'{database_name=}')
#     print(f'{wtf_seckey=}')
#     print(f'{bot_token=}')
#     print(f'{channel_id=}')

try:
    work_path = os.environ['APP_DIR']
except:
    work_path=''

if user == 'DEV':
    str_sqlite = f'sqlite://{work_path}/database/news.sqlite3'
    # print(f'{str_sqlite}')
    app.config['SQLALCHEMY_DATABASE_URI'] = str_sqlite
else:
    # print('!!!!!!!!')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pymssql://{user}:{password}@{server}/{database_name}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# appFL..config.from_object('config')

app.config['SECRET_KEY'] = hashlib.sha1(wtf_seckey).hexdigest()

db_main = SQLAlchemy(app)


# from app import views
