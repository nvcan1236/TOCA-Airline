from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
# from flask_login import LoginManager

app = Flask(__name__)


toan_connect_string = "mysql+pymysql://root:%s@localhost/toca_db?charset=utf8mb4" % quote("Huutoan123@")



app.config["SQLALCHEMY_DATABASE_URI"] = toan_connect_string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

app.config['SECRET_KEY'] = 'askrdghasdjfgakdsfuhgjhdsLGHU'

# login = LoginManager(app=app)