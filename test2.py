#!/usr/bin/env python3
from flask import Flask

import DataModel


def createApp(**kwargs):
    if not "debug" in kwargs: kwargs["debug"] = True
    app = Flask(__name__)
    return app

if __name__ == '__main__':
    app = createApp()
    db_engine, db_session = DataModel.createDB(app)
    for tpl in db_session.query(DataModel.Templates):
        print(tpl)
    app.run(debug=True)
