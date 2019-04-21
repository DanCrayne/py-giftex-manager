import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

attendance = db.Table('attendance', 
    db.Column('person_id', db.Integer, db.ForeignKey('people.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'))
)

class Person(db.Model):
    __tablename__ = 'people'
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(64), unique=False)
    events = db.relationship('Event',
                             secondary=attendance,
                             backref=db.backref('people', lazy='dynamic'),
                             lazy='dynamic')

    def __repr__(self):
        return '<Person %r' % self.name

class Event(db.Model):
    __tablename__ = 'events'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(64), unique=False)
    location        = db.Column(db.Text)
    date_and_time   = db.Column(db.DateTime)
