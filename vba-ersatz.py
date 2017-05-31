#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import flask
from flask import Flask, make_response
from flask_restful import Resource, Api, reqparse, request

import DataModel

app = Flask(__name__)

def createApi():
    api = Api(app)
    api.add_resource(Homepage, '/', "/index.html")
    api.add_resource(About, '/about', "/about.html")
    api.add_resource(Gruppe, "/gruppe/<int:nummer>", "/gruppe/<int:gid>/<string:command>")
    return api


def render_template(name, **kwargs):
    """Rendert das Template und versucht den Content-Type zu erraten. Dies wird benötigt, da flask-restful das nicht selber kann."""
    tpl = flask.render_template(name, **kwargs)
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


class Gruppe(Resource):
    def get(self, nummer, command="edit"):
        app.logger.debug("GET: %s gruppe %d" % (command, nummer))
        app.logger.debug("header: %s" % request.headers.get("Accept"))

        gruppe = db_session.query(DataModel.Gruppe).filter(DataModel.Gruppe.nummer == nummer).first()
        if gruppe is not None:
            if "/html" in request.headers["Accept"]:
                result = render_template("gruppe.html", gruppe=gruppe)
            elif "/json" in request.headers["Accept"]:
                result = render_template("gruppe.json", gruppe=gruppe)
            else:
                result = "Inkompatibler Accept-Header: %s" % request.headers["Accept"]
            return result
        else:
            return "Gruppe %d existiert nicht" % nummer, 404

    def post(self, nummer, command="edit"):
        app.logger.debug("POST: %s gruppe %d" % (command, nummer))

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Name der Gruppe')
        parser.add_argument('status', type=str, help='Status der Gruppe')
        args = parser.parse_args()

        neueGruppe = DataModel.Gruppe(nummer=nummer, name=args["name"], status=args["status"])
        db_session.add(neueGruppe)
        db_session.commit()

        return "OK"

class About(Resource):
    def get(self):
        app.logger.debug("about")
        result = render_template("about.html")
        return result

if __name__ == "__main__":
    api = createApi()
    db_engine, db_session = DataModel.createDB(app)
    app.run(debug=True)
