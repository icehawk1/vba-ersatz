#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def hello():
    return "Hey ho!"


@app.route("/about")
@app.route("/about.html")
def about():
    app.logger.debug("about")
    return render_template("about.html")

if __name__ == "__main__":
    app.run()
