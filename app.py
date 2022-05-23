from flask import Flask, request
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URL'] = config.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"]  = True


@app.route('/')
def hello():
    return 'Hello, My First Flask!'

@app.route('/companies')
class CompanyPostListGetView(Resource):

    def post(self):
        # 새로운 회사를 추가합니다.
        pass

    def get(self):
        # 회사들 리스트를 조회합니다.
        pass


@app.route('/companies/<string:company_name>')
class CompanyDeatilGetView(Resource):

    def get(self, company_name):
        # 회사 이름으로 검색합니다.
        pass

    def put(self, company_name):
        # 회사 이름으로 데이터를 수정합니다.
        pass

    def delete(self, company_name):
        # 회사 이름으로 데이러틑 삭제합니다.
        pass


@app.route('/search')
class SearchView(Resource):
    def get(self):
        # 자동완성 검색을 합니다.
        pass



