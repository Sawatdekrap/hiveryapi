from flask import request
from flask_restplus import Namespace, Resource, fields, reqparse, inputs
from hivery.services import get_common_friends, get_favourite_foods

api = Namespace('person')


person_schema = api.model('person', {
    'name': fields.String(required=True, description='person name'),
    'index': fields.Integer(required=True, description='person index'),
    'guid': fields.String(required=True, description='person guid'),
    'email': fields.String(required=True, description='person email'),
})
common_friends_schema = api.model('common_friends', {
    'person_a': fields.Nested(person_schema, required=True),
    'person_b': fields.Nested(person_schema, required=True),
    'friends': fields.List(fields.Nested(person_schema), required=True),
})

# Define a parser to grab query filters from query args
friends_parser = reqparse.RequestParser()
friends_parser.add_argument('has_died', type=inputs.boolean, location='args')
friends_parser.add_argument('gender', choices=('male', 'female'), location='args')
friends_parser.add_argument('age', type=int, location='args')
friends_parser.add_argument('eye_color', type=str, location='args')

@api.route('/<int:person_id>/common_friends/<int:friend_id>')
class CommonFriends(Resource):
    @api.expect(friends_parser)
    @api.marshal_with(common_friends_schema)
    def get(self, person_id, friend_id):
        # Get query filters from query args as specified by friends_parser
        filter_args = friends_parser.parse_args()
        
        data = get_common_friends(person_id, friend_id, **filter_args)
        return data


foods_schema = api.model('foods', {
    'name': fields.String(required=True, description='person name'),
    'age': fields.Integer(required=True, description='person age'),
    'fruits': fields.List(fields.String(attribute='name'), required=True, description='person favourite fruits'),
    'vegetables': fields.List(fields.String(attribute='name'), required=True, description='person favourite vegetables'),
})

@api.route('/<int:person_id>/favourite_foods')
class FavouriteFoods(Resource):
    @api.marshal_with(foods_schema)
    def get(self, person_id):
        return get_favourite_foods(person_id)
