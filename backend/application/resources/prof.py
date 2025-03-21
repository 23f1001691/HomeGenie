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

class ProfessionalAPI(Resource):
    # @jwt_required()
    @cache.cached(timeout = 5, key_prefix='professional_data')
    def get(self, professional_id):
        professional = Professional.query.get(professional_id)
        
        if not professional:
            return {"message": "Professional_id not found"}, 404
        
        if professional.resume and os.path.exists(professional.resume):
            try:
                filename = os.path.basename(professional.resume)
                professional.resume = url_for('serve_resume', filename=filename, _external=True)

            except Exception as e:
                return {"message": f"Failed to retrieve the PDF: {str(e)}"}, 500
        else:
            professional.resume = None

        if professional.profile_pic and os.path.exists(professional.profile_pic):
            try:
                filename = os.path.basename(professional.profile_pic)
                professional.profile_pic = url_for('serve_profile', filename=filename, _external=True)
            except Exception as e:
                return {"message": f"Failed to retrieve the Profile: {str(e)}"}, 500
        else:
            professional.profile_pic = None

        return marshal(professional, prof_resource_fields), 200

    # @jwt_required()
    # @role_required(["professional","admin"])
    def put(self, professional_id):
        professional = Professional.query.get(professional_id)

        if not professional:
            return {"message": "Professional_id not found"}, 404
    
        if 'profile_pic' in request.files:
            profile = request.files['profile_pic']
            
            if profile.filename == '':
                return {"message": 'No selected profile'}, 400
            
            if not profile_format(profile.filename):
                return {"message": 'File type not allowed'}, 400

            filename = secure_filename(profile.filename)
            path = os.path.join('application/static/profile/', filename)
            os.makedirs(os.path.dirname(path), exist_ok=True) 
            profile.save(path)
            professional.profile_pic = path

        if request.form:
            data = request.form.to_dict()
        else:
            data = prof_resource_parser.parse_args()

        original_status = professional.status

        for key,value in data.items():
            if value is not None:
                setattr(professional, key, value)

        if original_status != professional.status and professional.status == "Approved":

            if not professional.service_id:
                service = Service.query.filter_by(name=professional.service_name).first()
                if not service:
                    professional.status = "Unapproved"
                    return {"message": "Professional can't be approved as the service_name doesn't exist."}, 400
                
                professional.service_id = service.id

            #Send a mail saying that resume is approved

        if original_status != professional.status and professional.status == "Rejected":
            #Send a mail saying that resume is rejected
            pass            

        db.session.commit()
            
        return {"message":"Professional details updated"}, 200
    
    @jwt_required()
    @role_required(["professional","admin"])
    def delete(self, professional_id):
        professional = Professional.query.get(professional_id)
        if not professional:
            return {"message":"Professional_id not found"}, 404
        db.session.delete(professional.user)
        db.session.commit()
        return {"message":"Professional_id removed from database"}, 204
 
class ProfessionalListAPI(Resource):
    # @jwt_required()
    @cache.cached(timeout = 5, key_prefix='professional_list')
    def get(self):
        professionals = Professional.query.all()
        if not professionals:
            return {"message":"No professionals available"},404
        
        for prof in professionals:
            if prof.profile_pic and os.path.exists(prof.profile_pic):
                filename = os.path.basename(prof.profile_pic)
                prof.profile_pic = url_for('serve_profile', filename=filename, _external=True)
            else:
                prof.profile_pic = None     
                
        return marshal(professionals, prof_resource_fields), 201

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

api.add_resource(ProfessionalAPI, '/professional/<int:professional_id>')
api.add_resource(ProfessionalListAPI, '/professionals')

