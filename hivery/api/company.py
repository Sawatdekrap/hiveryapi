"""
- Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.
- Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.
- Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`
"""

from flask_restplus import Namespace, Resource, fields
from hivery.services import get_company_employees


api = Namespace('company')

"""
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
    company_id = db.Column(db.Integer, ForeignKey("Company.index"), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    registered = db.Column(db.DateTime, nullable=False)
    about = db.Column(db.String)
    greeting = db.Column(db.String)
"""
employee_schema = api.model('employee', {
    'name': fields.String(required=True, description='employee name'),
    'index': fields.Integer(required=True, description='employee index'),
    'guid': fields.String(required=True, description='employee guid'),
    'email': fields.String(required=True, description='employee email'),
})


@api.route('/<int:company_id>/employees')
class CompanyEmployees(Resource):
    @api.marshal_list_with(employee_schema)
    def get(self, company_id):
        return get_company_employees(company_id)
