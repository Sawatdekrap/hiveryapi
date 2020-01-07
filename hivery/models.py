from sqlalchemy import ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from flask.cli import with_appcontext
import click
import json
import os
import datetime
import decimal


db = SQLAlchemy()


class Company(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    employees = db.relationship('Person', back_populates='company')


class Person(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    _id = db.Column(db.String(24), unique=True, nullable=False)
    guid = db.Column(db.String(16), unique=True, nullable=False)
    has_died = db.Column(db.Boolean, nullable=False)
    balance = db.Column(db.Integer)  # Note this is cents and not dollars - see conversion in init_db
    picture = db.Column(db.String(80))
    name = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(16), nullable=False)
    age = db.Column(db.Integer)
    eyeColor = db.Column(db.String(16))
    company_id = db.Column(db.Integer, ForeignKey("company.index"))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(12))
    address = db.Column(db.String(80))
    registered = db.Column(db.DateTime, nullable=False)
    about = db.Column(db.String)
    greeting = db.Column(db.String)

    company = db.relationship('Company', back_populates='employees')
    tags = db.relationship('Tag')
    friends = db.relationship('Person', secondary='friend', primaryjoin='Person.index==friend.c.person_id', secondaryjoin='Person.index==friend.c.friend_id')
    fruits = db.relationship('Food', primaryjoin='and_(Person.index==food.c.person_id, food.c.type=="fruit")')
    vegetables = db.relationship('Food', primaryjoin='and_(Person.index==food.c.person_id, food.c.type=="vegetable")')


class Tag(db.Model):
    person_id = db.Column(db.Integer, ForeignKey("person.index"), primary_key=True)
    text = db.Column(db.String(32), primary_key=True)


class Friend(db.Model):
    person_id = db.Column(db.Integer, ForeignKey("person.index"), primary_key=True)
    friend_id = db.Column(db.Integer, ForeignKey("person.index"), primary_key=True)


class Food(db.Model):
    person_id = db.Column(db.Integer, ForeignKey("person.index"), primary_key=True)
    type = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(32), primary_key=True)


def create_db_from_resources():
    """Load database from resources directory
    
    It is assumed that the following files are present in the given directory:
    companies.json, people.json, food.json.
    Can raise sqlalchemy.exc.SQLAlchemyError if database transaction fails.
    """
    db.create_all()

    # Load company objects into list to be committed
    resources_dir = current_app.config['RESOURCES_DIR']
    company_file = os.path.join(resources_dir, 'companies.json')
    with open(company_file, 'r') as f:
        data = json.load(f)
    companies = [Company(index=company['index'], name=company['company']) for company in data]

    # Read 
    people_file = os.path.join(resources_dir, 'people.json')
    with open(people_file, 'r') as f:
        data = json.load(f)
    people = []
    tags = []
    friends = []
    food = []
    person_keys = [c.name for c in Person.__table__.columns]
    
    food_file = os.path.join(resources_dir, 'food.json')
    with open(food_file, 'r') as f:
        food_type_mapping = json.load(f)

    for person in data:
        # Clean person dict by stripping unused keys and formatting values
        person_dict = {k: person[k] for k in person_keys}
        # Strip extra characters and convert to cents
        balance_str = person_dict['balance'].replace('$', '').replace(',', '')
        balance_dec = decimal.Decimal(balance_str) * 100
        person_dict['balance'] = int(balance_dec)
        # Clean registered datetime string to convert to datetime object for sqlalchemy
        registered = person_dict['registered']
        registered_utc_alter = registered[:-3] + registered[-2:]  # Remove the ':' to be able to parse UTC offset
        person_dict['registered'] = datetime.datetime.strptime(registered_utc_alter, '%Y-%m-%dT%H:%M:%S %z')  # 2016-07-13T12:29:07 -10:00

        people.append(Person(**person_dict))
        # Create associated tags, friends, foods for this person object
        for tag in set(person['tags']):
            tags.append(Tag(person_id=person['index'], text=tag))
        for friend in person['friends']:
            friends.append(Friend(person_id=person['index'], friend_id=friend['index']))
        for item in set(person['favouriteFood']):
            food.append(Food(person_id=person['index'], type=food_type_mapping[item], name=item))

    db.session.add_all(companies)
    db.session.add_all(people)
    db.session.add_all(food)
    db.session.add_all(friends)
    db.session.add_all(tags)

    # Try to commit changes, but rollback transaction on failure
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise


@click.command('db-init')
@with_appcontext
def db_init():
    """Wrapper around load_db_from_resources to be called from cli"""
    create_db_from_resources()
