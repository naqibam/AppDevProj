from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,
                   primary_key = True)

    username = db.Column(db.String(20),
                         unique = True,
                         nullable = False)
    email = db.Column(db.String(120),
                      unique = True,
                      nullable = False)
    password = db.Column(db.String(60),
                         nullable = False)
