#!/usr/bin/env python3
from flask import Flask, request
from flask_restful import Resource, Api
from DataModel import Templates
from flask_sqlalchemy import SQLAlchemy


if __name__ == '__main__':
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db = SQLAlchemy()
    db.init_app(app)
    db.create_all() # <----

    api = Api(app)
    api.add_resource(TodoSimple, '/<string:todo_name>')

    templates = Templates.query.all()
    print(templates)
    app.run(debug=True)
