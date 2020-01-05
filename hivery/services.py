from sqlalchemy.orm import joinedload, aliased
from flask_restplus import abort
from hivery.models import db, Company, Person, Friend, Food


def get_company_employees(company_id):
    employees = (
        db.session.query(Person)
        .filter(Person.company_id==company_id)
        .all()
    )
    return employees


def get_common_friends(person_a_id, person_b_id):
    friends_a = (
        db.session.query(Person)
        .join(Friend, Person.index==Friend.friend_id)
        .filter(Friend.person_id==person_a_id)
    )
    friends_b = (
        db.session.query(Person)
        .join(Friend, Person.index==Friend.friend_id)
        .filter(Friend.person_id==person_b_id)
    )

    common = (
        friends_a
        .intersect(friends_b)
        .filter(Person.eyeColor=='brown')
        .filter(Person.has_died==False)
        .all()
    )
    return common


def get_favourite_foods(person_id):
    fruit = aliased(Food)
    vegetables = aliased(Food)
    data = (
        db.session.query(Person)
        .options(joinedload(Person.fruits))
        .options(joinedload(Person.vegetables))
        .filter(Person.index==person_id)
        .one_or_none()
    )
    return data
