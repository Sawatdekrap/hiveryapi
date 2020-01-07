"""All endpoints for the company api namespace"""
from flask_restplus import Namespace, Resource, fields
from hivery.services import get_company_employees, get_companies


api = Namespace('company')

company_schema = api.model('company', {
    'index': fields.Integer(required=True, description='company index'),
    'name': fields.String(required=True, description='company name'),
})
@api.route('/')
class CompanyRoot(Resource):
    @api.marshal_list_with(company_schema)
    def get(self):
        return get_companies()


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
