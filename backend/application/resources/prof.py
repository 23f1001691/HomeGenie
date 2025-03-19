from flask_restful import Resource, reqparse, fields, marshal, request
from application.extensions import api, db, bcrypt, cache
from application.models import Professional, User, Service, ServiceRequest
from flask import url_for
import os
from werkzeug.utils import secure_filename
from application.utils import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.utils import profile_format, resume_format, format_date

prof_resource_parser = reqparse.RequestParser()
prof_resource_parser.add_argument('id', type=int, help='Error: {error_msg}')
prof_resource_parser.add_argument('user_id', type=int, help='Error: {error_msg}')
prof_resource_parser.add_argument('service_id', type=int, help='Error: {error_msg}')
prof_resource_parser.add_argument('name', type=str, help='Error: {error_msg}')
prof_resource_parser.add_argument('service_name', type=str, help='Error: {error_msg}')
prof_resource_parser.add_argument('contact_no', type=int, help='Error: {error_msg}')
prof_resource_parser.add_argument('experience', type=str, help='Error: {error_msg}')
prof_resource_parser.add_argument('description', type=str, help='Error: {error_msg}')
prof_resource_parser.add_argument('address', type=str, help='Error: {error_msg}')
prof_resource_parser.add_argument('pincode', type=int, help='Error: {error_msg}')
prof_resource_parser.add_argument('status', type=str, help='Error: {error_msg}')
prof_resource_parser.add_argument('rating', type=float, help='Error: {error_msg}')
prof_resource_parser.add_argument('flag', type=bool, help='Error: {error_msg}')
prof_resource_parser.add_argument('category', type=str, help='Error: {error_msg}')

prof_resource_fields = {
    'id': fields.Integer,
    'user_id':fields.Integer,
    'service_id': fields.Integer,
    'name': fields.String,
    'service_name': fields.String,
    'contact_no':fields.Integer,
    'experience': fields.String,
    'description':fields.String,
    'resume': fields.String,
    'created_date': fields.String(attribute=lambda x: format_date(x.created_date)),
    'profile_pic':fields.String,
    'address': fields.String,
    'pincode': fields.Integer,
    'status': fields.String,
    'rating':fields.Float,
    'flag':fields.Boolean,
    'category': fields.String
}

class ProfessionalListAPI(Resource):
    def post(self):
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        name = request.form.get('name', None)
        service_name = request.form.get('service_name', None)
        category = request.form.get('category', None)

        if not all([email, password, name, service_name, category]):
            return {"message": "All details not provided"}, 400

        if 'resume' not in request.files:
            return {'message':'No file exists'}, 400
        
        resume = request.files['resume']

        if resume.filename == '':
                return {'message':'No selected file'}, 400
        
        if not resume_format(resume.filename):
            return {'message': 'File type not allowed, only PDFs are allowed'}, 400
        
        if User.query.filter_by(email=email).first():
            return {"message": "User already exists"}, 409
        
        resume_path = None
        path = os.path.join('application/static/resume/', secure_filename(resume.filename))
        os.makedirs(os.path.dirname(path), exist_ok=True)  

        try:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            resume.save(path)
            resume_path = path
            new_user = User(email=email, password=hashed_password, role='professional')
            db.session.add(new_user)
            db.session.flush()  
            
            new_professional = Professional(user_id=new_user.id, name=name, category=category,
                                            service_name=service_name, resume=resume_path)
            db.session.add(new_professional)
            db.session.commit()

            return {"message": "Customer created successfully"}, 201
        
        except Exception as e:
            db.session.rollback()
            if os.path.exists(path):
                os.remove(path)
            return {"message": str(e)}, 500 
    
api.add_resource(ProfessionalListAPI, '/professionals')

