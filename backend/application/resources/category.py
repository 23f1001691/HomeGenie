from flask_restful import Resource, fields, marshal
from application.extensions import api
from application.models import Category

category_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'image_url': fields.String,
}

class CategoriesAPI(Resource):
    def get(self):
        categories = Category.query.all()
        if not categories:
            return {"message": "No categories available"}, 404

        return marshal(categories, category_resource_fields), 201
        
api.add_resource(CategoriesAPI, '/categories')

