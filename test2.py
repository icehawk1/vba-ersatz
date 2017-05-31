#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from DataModel import Templates

if __name__ == '__main__':
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db = SQLAlchemy()
    db.init_app(app)
    db.create_all() # <----

    templates = Templates.query.all()
    print(templates)
    app.run(debug=True)
