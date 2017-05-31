#!/usr/bin/env python3
from enum import Enum

import sqlalchemy
from sqlalchemy import Integer, String, Column, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


def createDB(app):
    engine = create_engine('sqlite:////tmp/test.db', echo=False)
    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()
    Base.metadata.create_all(engine)
    return engine, session

class _Status(Enum):
    """Enum der festlegt in welchen Zuständen ein Testcase oder eine Gruppe sein kann"""
    todo = 1 # Noch zu erledigen
    implemented = 2 # Wurde implementiert, aber noch nicht an Microsens ausgeliefert
    released = 3 # Wurde an Microsens ausgeliefert


class Gruppe(Base):
    """Eine Gruppe von Testcases die gemeinsam ausgeführt wird und üblicherweise immer einen Namespace abdeckt"""
    __tablename__ = 'gruppen'
    gid = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False, doc="Der Name dieser Gruppe")
    testcases = relationship("Testcase",
                             doc="Die zu dieser Gruppe gehörenden Testcases. Ein Testcase kann immer nur zu einer Gruppe gehören.")
    status = Column(sqlalchemy.Enum("_Status"),
                    doc="Ob die Gruppe bereits implementiert/released wurde oder ob dies noch ein TODO ist")


class Testcase(Base):
    __tablename__ = 'testcases'
    tid = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False, doc="Der Testcasename wie im Testplan")
    status = Column(sqlalchemy.Enum("_Status"),
                    doc="Ob der Testcase bereits implementiert/released wurde oder ob dies noch ein TODO ist")
    gid = Column(Integer, ForeignKey(Gruppe.__tablename__ + ".gid"))
    parameters = relationship("TestcaseParameter", collection_class=ordering_list('num'))


class TestcaseParameter(Base):
    __tablename__ = 'parameters'
    tpid = Column(Integer, primary_key=True)
    value = Column(String(2048), nullable=False, doc="Der Wert dieses Parameters, wie er im Testplan auftauchen wird")
    num = Column(Integer, doc="Dient dazu, die Reihenfolge der Parameter in der DB zu speichern.")
    tid = Column(Integer, ForeignKey(Testcase.__tablename__ + ".tid"))


class Templates(Base):
    __tablename__ = 'templates'
    tid = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    beschreibung = Column(String(2048), nullable=True, doc="Nähere Beschreibung wie dieses Template anzuwenden ist.")
