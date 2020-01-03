from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import click
import json
import os
import datetime


db = SQLAlchemy()


class Company(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)


class Person(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    _id = db.Column(db.String(24), unique=True, nullable=False)
    guid = db.Column(db.String(16), unique=True, nullable=False)
    has_died = db.Column(db.Boolean, nullable=False)
    balance = db.Column(db.Numeric(10, 2), nullable=False)
    picture = db.Column(db.String(80))
    name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    age = db.Column(db.Integer)
    eyeColor = db.Column(db.String(20))
    company_id = db.Column(db.Integer, ForeignKey("company.index"), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    registered = db.Column(db.DateTime, nullable=False)
    about = db.Column(db.String)
    greeting = db.Column(db.String)


class Tag(db.Model):
    person_id = db.Column(db.Integer, ForeignKey("person.index"), primary_key=True)
    text = db.Column(db.String(20), primary_key=True)


class Friend(db.Model):
    person_id = db.Column(db.Integer, ForeignKey("person.index"), primary_key=True)
    friend_id = db.Column(db.Integer, ForeignKey("person.index"), primary_key=True)


class Food(db.Model):
    person_id = db.Column(db.Integer, ForeignKey("person.index"), primary_key=True)
    type = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(32), primary_key=True)


@click.command('init-db')
@with_appcontext
def init_db():
    db.create_all()

    resource_dir = 'resources'
    company_file = os.path.join(resource_dir, 'companies.json')
    with open(company_file, 'r') as f:
        data = json.load(f)
    companies = [Company(index=company['index'], name=company['company']) for company in data]

    people_file = os.path.join(resource_dir, 'people.json')
    with open(people_file, 'r') as f:
        data = json.load(f)
    people = []
    tags = []
    friends = []
    food = []
    person_keys = [c.name for c in Person.__table__.columns]
    for person in data:
        # Clean person dict by stripping unused keys and formatting values
        person_dict = {k: person[k] for k in person_keys}
        person_dict['balance'] = person_dict['balance'].replace('$', '').replace(',', '')
        registered = person_dict['registered']
        registered_utc_alter = registered[:-3] + registered[-2:]
        person_dict['registered'] = datetime.datetime.strptime(registered_utc_alter, '%Y-%m-%dT%H:%M:%S %z') # 2016-07-13T12:29:07 -10:00

        people.append(Person(**person_dict))
        for tag in set(person['tags']):
            tags.append(Tag(person_id=person['index'], text=tag))
        for friend in person['friends']:
            friends.append(Friend(person_id=person['index'], friend_id=friend['index']))
        for item in set(person['favouriteFood']):
            # TODO correctly parse type
            food.append(Food(person_id=person['index'], type='fruit', name=item))
    
    db.session.add_all(companies)
    db.session.add_all(people)
    db.session.add_all(food)
    db.session.add_all(friends)
    db.session.add_all(tags)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise
