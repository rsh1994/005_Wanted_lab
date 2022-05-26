from flask import jsonify, make_response
from flask_restful import Resource, request

from .models import *

class CompanyList(Resource):
    def get(self):
        country_code = request.headers.get("x-wanted_language", "ko")
        company_name = request.args.get("query")