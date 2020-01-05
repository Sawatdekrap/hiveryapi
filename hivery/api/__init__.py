from flask_restplus import Api
from hivery.api.person import api as person_ns
from hivery.api.company import api as company_ns


api = Api()

api.add_namespace(person_ns, path='/person')
api.add_namespace(company_ns, path='/company')
