from flask_restful import Resource, reqparse, fields, marshal, request
from application.extensions import api, db, bcrypt, cache
from flask import url_for
from werkzeug.utils import secure_filename
from application.models import Customer, User, ServiceRequest
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.utils import role_required
import os
from sqlalchemy import or_

customer_resource_parser = reqparse.RequestParser(bundle_errors=True)
customer_resource_parser.add_argument('id', type=int, help='Error: {error_msg}')
customer_resource_parser.add_argument('user_id', type=int, help='Error: {error_msg}')
customer_resource_parser.add_argument('email', type=str, help='Error: {error_msg}')
customer_resource_parser.add_argument('password', type=str, help='Error: {error_msg}')
customer_resource_parser.add_argument('name', type=str, help='Error: {error_msg}')
customer_resource_parser.add_argument('contact_no', type=int, help='Error: {error_msg}')
customer_resource_parser.add_argument('address', type=str, help='Error: {error_msg}')
customer_resource_parser.add_argument('pincode', type=int, help='Error: {error_msg}')
customer_resource_parser.add_argument('flag', type=bool, help='Error: {error_msg}')

customer_resource_fields = {
    'id': fields.Integer,
    'user_id':fields.Integer,
    'name': fields.String,
    'contact_no':fields.Integer,
    'address': fields.String,
    'pincode': fields.Integer,
    'profile_pic':fields.String,
    'flag':fields.Boolean
}
  
class CustomerListAPI(Resource):
    def post(self):
        data = customer_resource_parser.parse_args()
        email = data.get('email', None)
        password = data.get('password', None)
        name = data.get('name', None)
        contact_no = data.get('contact_no', None)

        if not all([email, password, name, contact_no]):
            return {"message": "All details not provided"}, 400

        if User.query.filter_by(email=email).first():
            return {"message": "User already exists"}, 409

        try:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(email=email, password=hashed_password, role='customer')
            db.session.add(new_user)
            db.session.flush()  

            new_customer = Customer(user_id=new_user.id, name=name, contact_no=contact_no)
            db.session.add(new_customer)
            db.session.commit()

            return {"message": "Customer created successfully"}, 201
        
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500 
    
api.add_resource(CustomerListAPI, '/customers')

