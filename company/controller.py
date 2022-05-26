from flask import jsonify, make_response
from flask_restful import Resource, request

from .models import *

class CompanyList(Resource):
    def get(self):
        country_code = request.headers.get("x-wanted_language", "ko")
        company_name = request.args.get("query")

        country = Country.query.filter_by(name=country_code).first()

        if country is None:
            return {"message": "COUNTRY_NOT_SUPPORTED"}, 404

        selected_companies = (
            db.session.query(company_countries).filter_by(country_id=country.id).all()
        )

        result = [
            {"company_name": company.translated_name}
            for company in selected_companies
            if company_name in company.translated_name
        ]

        if len(result) == 0:
            return {"message": "COMPANY NOT FOUND"}, 404

        return result, 200


class CompanyDetail(Resource):
    def get(self, comp_name):
        header = request.headers.get("x-wanted-language", "ko")

        company = Company.query.filter_by(name=comp_name).first()
        country = Country.query.filter_by(name=header).first()

        if not company or not country:
            return make_response(
                jsonify({"message": "Company or Language Not Found"}), 404
            )

        company_country = (
            db.session.query(company_countries)
            .filter_by(company_id=company.id, country_id=country.id)
            .first()
        )

        if not company_country:
            return make_response(jsonify({"message": "Company Does Not Exist"}), 404)

        company_tag_set = db.session.query(company_tags).filter_by(
            company_id=company.id
        )
        country_tag_list = [
            db.session.query(country_tags)
            .filter_by(country_id=country.id, tag_id=t.tag_id)
            .first()
            .translated_tag
            for t in company_tag_set
        ]

        return make_response(
            jsonify(
                {
                    "company_name": company_country.translated_name,
                    "tags": [tag for tag in country_tag_list],
                }
            ),
            200,
        )


class CompanyCreateView(Resource):
    def post(self):
        FIRST_INPUT = 0
        VALUE_IDX = 1

        data = request.get_json()
        country_code = request.headers.get("x-wanted-language")

        country = Country.query.filter_by(name=country_code).first()

        if not country:
            country = Country(name=country_code)
            db.session.add(country)

        company_infos = list(data["company_name"].items())
        company = Company.query.filter_by(
            name=company_infos[FIRST_INPUT][VALUE_IDX]
        ).first()
        
        if company:
            return {"message": "Company Already Exist"}, 404

        else:
            company = Company(name=company_infos[FIRST_INPUT][VALUE_IDX])
            db.session.add(company)

        for country, name in company_infos:
            company_countries_query = company_countries.insert().values(
                country_id=Country.query.filter_by(name=country).first().id,
                company_id=company.id,
                translated_name=name,
            )
            db.session.execute(company_countries_query)

        tag_list = []
        for tags in data["tags"]:
            tag_infos = list(tags["tag_name"].items())
            tag = Tag.query.filter_by(name=tag_infos[FIRST_INPUT][VALUE_IDX]).first()

            if not tag:
                print("tag is None")
                tag = Tag(name=tag_infos[FIRST_INPUT][VALUE_IDX])
                db.session.add(tag)

            for country, name in tag_infos:
                if country_code == country:
                    tag_list.append(name)

                country_tags_query = country_tags.insert().values(
                    country_id=Country.query.filter_by(name=country).first().id,
                    tag_id=tag.id,
                    translated_tag=name,
                )
                db.session.execute(country_tags_query)

            company_tags_query = company_tags.insert().values(
                company_id=company.id,
                tag_id=tag.id,
            )
            db.session.execute(company_tags_query)

        db.session.commit()
        return {"company_name": data["company_name"][country_code], "tags": tag_list}, 200
