#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import flask
from flask import Flask, make_response
from flask_restful import Resource, Api, reqparse, request

import DataModel

app = Flask(__name__)
gruppen_argparser = reqparse.RequestParser()
gruppen_argparser.add_argument('nummer', type=int, help='Nummer der Gruppe')
gruppen_argparser.add_argument('name', type=str, help='Name der Gruppe')
gruppen_argparser.add_argument('status', type=str, help='Status der Gruppe')

def createApi():
    api = Api(app)
    api.add_resource(Homepage, '/', "/index.html")
    api.add_resource(About, '/about', "/about.html")
    api.add_resource(NeueGruppe, "/gruppe", "/gruppe/")
    api.add_resource(Gruppe, "/gruppe/<int:gid>", "/gruppe/<int:gid>/<string:command>")
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


class NeueGruppe(Resource):
    """Resource zum anlegen einer neuben Gruppe. Dies wird getrennt von der Resource zum bearbeiten von spezifischen Gruppen geführt,
    da es sonst leicht zu versehentlichen Änderungen an bestehenden Gruppen, bzw. versehentlichem neu anlegen kommen kann."""

    def get(self):
        result = render_template("neue_gruppe.html")
        return result

    def post(self):
        args = gruppen_argparser.parse_args()
        if db_session.query(DataModel.Gruppe).filter(DataModel.Gruppe.nummer == args["nummer"]).count() > 0:
            return "Gruppe %d existiert bereits" % args["nummer"], 409

        neueGruppe = DataModel.Gruppe(nummer=args["nummer"], name=args["name"], status=args["status"])
        db_session.add(neueGruppe)
        db_session.commit()

        return "Gruppe wurde angelegt"

class Gruppe(Resource):
    def get(self, gid, command="edit"):
        app.logger.debug("GET: %s gruppe %d" % (command, gid))
        app.logger.debug("header: %s" % request.headers.get("Accept"))

        gruppe = db_session.query(DataModel.Gruppe).filter(DataModel.Gruppe.gid == gid).first()
        if gruppe is not None:
            if "/html" in request.headers["Accept"]:
                result = render_template("gruppe.html", gruppe=gruppe)
            elif "/json" in request.headers["Accept"]:
                result = render_template("gruppe.json", gruppe=gruppe)
            else:
                result = "Inkompatibler Accept-Header: %s" % request.headers["Accept"]
            return result
        else:
            return "Gruppe %d existiert nicht" % gid, 404

    def post(self, gid, command="edit"):
        args = gruppen_argparser.parse_args()

        if db_session.query(DataModel.Gruppe).filter(DataModel.Gruppe.nummer == args["nummer"]).count() > 0:
            return "Gruppe %d existiert noch nicht" % args["nummer"], 404

        neueGruppe = DataModel.Gruppe(nummer=gid, name=args["name"], status=args["status"])
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
