#!/usr/bin/env python3
from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class TodoSimple(Resource):
    def get(self, todo_name):
        item = TodoItem.query.filter_by(name=todo_name).first()
        print(item)
        return item.__repr__()

    def put(self, todo_name):
        item = TodoItem(todo_name, request.form['data'])
        print("todo: %s" % item)
        db.session.add(item)
        db.session.commit()
        return item.__repr__()


api.add_resource(TodoSimple, '/<string:todo_name>')


class TodoItem(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    data = db.Column(db.String(120), unique=False)

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __repr__(self):
        return '{ "%s": "%s" }' % (self.name, self.data)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
