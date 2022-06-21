from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from core.app import app
from pydantic import Json


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://iwuser:iw2022@db_iw/iwdb"
db = SQLAlchemy(app)

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id: int = db.Column(db.Integer, primary_key=True)

    name: str = db.Column(db.String(50))
    graph1: float = db.Column(db.Float)
    graph2: float = db.Column(db.Float)
    graph3: float = db.Column(db.Float)
    date:datetime = db.Column(db.DateTime)


    def __repr__(self):
        return f"<name {self.name}>"

class Task(db.Model):
    __tablename__ = 'tasks'

    id: int = db.Column(db.Integer, primary_key=True)
    task_is: str = db.Column(db.String())
    data: Json = db.Column(db.JSON())
    date:datetime = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<name {self.name}>"

