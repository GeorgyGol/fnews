from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap, __version__
from flask_sqlalchemy import SQLAlchemy

from pathlib import Path

appFL = Flask(__name__)
bootstrap = Bootstrap(appFL)

# print('flask version', __version__)
# print('flask application', appFL.name)

from app.database.config import user, password, server, database_name

base_path = Path(Path(__file__).absolute().parent, 'database', 'news.sqlite3')
print('base-path = ', base_path.absolute(), )

appFL.config['SQLALCHEMY_DATABASE_URI'] = rf'sqlite:///{base_path.absolute()}'
# appFL.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pymssql://{user}:{password}@{server}/{database_name}'

appFL.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# appFL..config.from_object('config')


database = SQLAlchemy(appFL)