from flask_restful import Resource, fields, marshal
from application.extensions import api
from application.models import Category
import os 
from flask import url_for

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

        for category in categories:
            if category.image_url and os.path.exists(category.image_url):
                filename = os.path.basename(category.image_url)
                category.image_url = url_for('send_category', filename=filename, _external=True)
            else:
                category.image_url = None  

        return marshal(categories, category_resource_fields), 201
        
api.add_resource(CategoriesAPI, '/categories')

