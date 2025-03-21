from flask import send_from_directory, current_app as app, url_for
from flask_restful import Resource, reqparse, fields, marshal, request
from flask_jwt_extended import jwt_required
from application.utils import role_required
from application.models import Customer, Professional
from application.resources.prof import prof_resource_fields
from application.resources.customer import customer_resource_fields
import os 

# @jwt_required()
@app.get('/application/static/resume/<filename>')
def serve_resume(filename):
    return send_from_directory('static/resume', filename)

# @jwt_required()
@app.get('/profile/<filename>')
def serve_profile(filename):
    return send_from_directory('static/profile', filename)

# @jwt_required()
@app.get('/api/filter-users')
def filter_users():

    filter_by = request.args.get('filter_by','')
    search_query = request.args.get('search_query','')

    if filter_by == "Customers":

        customers = Customer.query.filter(Customer.name.ilike(f'%{search_query}%')).all()

        if not customers:
            return {"message":"No such user exists"},404

        for customer in customers:
            if customer.profile_pic and os.path.exists(customer.profile_pic):
                filename = os.path.basename(customer.profile_pic)
                customer.profile_pic = url_for('serve_profile', filename=filename, _external=True)
            else:
                customer.profile_pic = None   

        return marshal(customers,customer_resource_fields), 200

    elif filter_by == "Professionals":

        professionals = Professional.query.filter(Professional.name.ilike(f'%{search_query}%')).all()

        if not professionals:
            return {"message":"No such user exists"},404
        
        for prof in professionals:
            if prof.profile_pic and os.path.exists(prof.profile_pic):
                filename = os.path.basename(prof.profile_pic)
                prof.profile_pic = url_for('serve_profile', filename=filename, _external=True)
            else:
                prof.profile_pic = None  

        return marshal(professionals,prof_resource_fields), 200

    return {"message": "Invalid filter option"}, 400