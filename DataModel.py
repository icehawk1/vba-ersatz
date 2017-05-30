#!/usr/bin/env python3
from enum import Enum
from sqlalchemy.ext.orderinglist import ordering_list
from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()

class _Status(Enum):
    """Enum der festlegt in welchen Zuständen ein Testcase oder eine Gruppe sein kann"""
    todo = 1 # Noch zu erledigen
    implemented = 2 # Wurde implementiert, aber noch nicht an Microsens ausgeliefert
    released = 3 # Wurde an Microsens ausgeliefert

class Gruppe(db.Model):
    """Eine Gruppe von Testcases die gemeinsam ausgeführt wird und üblicherweise immer einen Namespace abdeckt"""
    gid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, doc="Der Name dieser Gruppe")
    testcases = db.relationship("Testcase", doc="Die zu dieser Gruppe gehörenden Testcases. Ein Testcase kann immer nur zu einer Gruppe gehören.")
    status = db.Column(db.Enum("_Status"), doc="Ob die Gruppe bereits implementiert/released wurde oder ob dies noch ein TODO ist")

class Testcase(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, doc="Der Testcasename wie im Testplan")
    status = db.Column(db.Enum(_Status), doc="Ob der Testcase bereits implementiert/released wurde oder ob dies noch ein TODO ist")
    gid = db.Column(db.Integer, db.ForeignKey("gruppe.gid"))
    parameters = db.relationship("TestcaseParameter", collection_class=ordering_list('num'))

class TestcaseParameter(db.Model):
    tpid = db.Column(db.Integer,primary_key=True)
    value = db.Column(db.String(2048), nullable=False, doc="Der Wert dieses Parameters, wie er im Testplan auftauchen wird")
    num = db.Column(db.Integer, doc="Dient dazu, die Reihenfolge der Parameter in der DB zu speichern.")
    tid = db.Column(db.Integer, db.ForeignKey("testcase.tid"))

class Templates(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    beschreibung = db.Column(db.String(2048), doc="Nähere Beschreibung wie dieses Template anzuwenden ist.")

if __name__ == "__main__":
    print("DataModel")

