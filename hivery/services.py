from sqlalchemy.orm import subqueryload, aliased
from flask_restplus import abort
from hivery.models import db, Company, Person, Friend, Food


def check_existance(table, row_id):
    """Helper function to get table row or abort"""
    instance = db.session.query(table).get(row_id)
    if instance is None:
        abort(404, 'No such %s exists with identifier %s' % (table.__name__, row_id))
    return instance


def get_companies():
    """Get all companies"""
    companies = db.session.query(Company).all()
    return companies


def get_person(person_id):
    """Get single person instance"""
    return check_existance(Person, person_id)


def get_company_employees(company_id):
    """Get employees for a given company"""
    check_existance(Company, company_id)
    employees = (
        db.session.query(Person)
        .filter(Person.company_id==company_id)
        .all()
    )
    return employees


def get_common_friends(person_a_id, person_b_id, has_died=None, gender=None, age=None, eye_color=None):
    """Get common friends between two people and optionally filtered
    
    Filters should be provided in the given keyword arguments.
    """
    person_a = check_existance(Person, person_a_id)
    person_b = check_existance(Person, person_b_id)

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
    query = friends_a.intersect(friends_b)

    # Apply optional filters
    if has_died is not None:
        query = query.filter(Person.has_died==has_died)
    if gender is not None:
        query = query.filter(Person.gender==gender)
    if age is not None:
        query = query.filter(Person.age==age)
    if eye_color is not None:
        query = query.filter(Person.eyeColor==eye_color)

    common_friends = query.all()
    return {'person_a': person_a, 'person_b': person_b, 'friends': common_friends}


def get_favourite_foods(person_id, **kwargs):
    """Get favourite fruits and vegetables of a person
    
    Join condition seen in Person model definition"""
    check_existance(Person, person_id)

    data = (
        db.session.query(Person)
        .options(subqueryload(Person.fruits))
        .options(subqueryload(Person.vegetables))
        .filter(Person.index==person_id)
        .one_or_none()
    )
    return data
