#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import flask
from flask import Flask, make_response
from flask_restful import Resource, Api

import DataModel

app = None


def createApp():
    app = Flask(__name__)
    return app


def createApi():
    api = Api(app)
    api.add_resource(Homepage, '/', "/index.html")
    api.add_resource(About, '/about', "/about.html")
    return api


def render_template(name, *args, **kwargs):
    """Rendert das Template und versucht den Content-Type zu erraten. Dies wird benötigt, da flask-restful das nicht selber kann."""
    tpl = flask.render_template("index.html", *args, **kwargs)
    response = make_response(tpl)
    if name.endswith(".html"):
        response.headers['Content-Type'] = 'text/html'
    elif name.endswith(".json"):
        response.headers['Content-Type'] = 'application/json'
    elif name.endswith(".xml"):
        response.headers['Content-Type'] = 'application/xml'
    else:
        response.headers["Content-Type"] = "text/plain"
    return response


class Homepage(Resource):
    def get(self):
        result = render_template("index.html")
        return result


class About(Resource):
    def get(self):
        app.logger.debug("about")
        result = render_template("about.html")
        return result

if __name__ == "__main__":
    app = createApp()
    api = createApi()
    db_engine, db_session = DataModel.createDB(app)
    app.run(debug=True)
