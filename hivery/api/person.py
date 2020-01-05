from flask_restplus import Namespace, Resource, fields
from hivery.services import get_common_friends, get_favourite_foods

api = Namespace('person')


friend_schema = api.model('friend', {
    'name': fields.String(required=True, description='person name'),
    'index': fields.Integer(required=True, description='person index'),
    'guid': fields.String(required=True, description='person guid'),
    'email': fields.String(required=True, description='person email'),
})

@api.route('/<int:person_id>/common_friends/<int:friend_id>')
class CommonFriends(Resource):
    @api.marshal_list_with(friend_schema)
    def get(self, person_id, friend_id):
        return get_common_friends(person_id, friend_id)



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
