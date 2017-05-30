#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Heyho!"


if __name__ == "__main__":
    app.run(debug=True)
