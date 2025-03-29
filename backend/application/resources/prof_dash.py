from flask_restful import Resource
from application.extensions import api, db, cache
from application.models import Professional, User, Service, ServiceRequest, Payment, Review
from flask import url_for
import os
from datetime import datetime
from application.utils import role_required
from flask_jwt_extended import jwt_required
from sqlalchemy import func

class ProfDashAPI(Resource):
    @jwt_required()
    @role_required(['professional'])
    @cache.cached(timeout = 5, key_prefix='professional_dashboard')
    def get(self, professional_id):
        professional = Professional.query.get(professional_id)
        
        if not professional:
            return {"message": "ProfessionalID not found"}, 404

        # if professional.profile_pic and os.path.exists(professional.profile_pic):
        #     try:
        #         filename = os.path.basename(professional.profile_pic)
        #         professional.profile_pic = url_for('serve_profile', filename=filename, _external=True)
        #     except Exception as e:
        #         return {"message": f"Failed to retrieve the Profile: {str(e)}"}, 500
        # else:
        #     professional.profile_pic = None

        # print(professional.profile_pic)

        rating = (db.session.query(func.avg(Review.rating)) 
            .join(ServiceRequest, ServiceRequest.id == Review.service_request_id) 
            .filter(ServiceRequest.professional_id == professional_id)  
            .scalar() or 0)

        rev_data, income = get_revenue_by_month(professional_id)
        req_data = get_request_count(professional_id)

        return {
            "name": professional.name,
            # "profile": professional.profile_pic,
            "description": professional.description,
            "service_name": professional.service_name,
            "rating": rating,
            "income": income,
            "rev_data": rev_data,
            "req_data": req_data
        }, 200

api.add_resource(ProfDashAPI, '/prof-dash/<int:professional_id>')

def get_revenue_by_month(professional_id):
    revenue_data = (
        db.session.query(
            func.extract('month', ServiceRequest.date_of_completion).label('month'),
            func.sum(Payment.amount).label('total_revenue')
        )
        .join(Payment, Payment.service_request_id == ServiceRequest.id)  
        .filter(ServiceRequest.professional_id == professional_id) 
        .group_by(func.extract('month', ServiceRequest.date_of_completion))  
        .order_by('month')  
        .all()  
    )

    monthly_revenue = [0.0] * 12 
    sum = 0
    for row in revenue_data:
        if row.month: 
            month_index = int(row.month) - 1  
            monthly_revenue[month_index] = float(row.total_revenue) if row.total_revenue else 0.0
            sum += float(row.total_revenue) if row.total_revenue else 0.0

    return monthly_revenue, sum

def get_request_count(professional_id):
    requested = int(db.session.query(func.count(ServiceRequest.id)).filter(
            ServiceRequest.status == 'Requested', ServiceRequest.professional_id == professional_id).scalar() or 0)
    rejected = int(db.session.query(func.count(ServiceRequest.id)).filter(
                ServiceRequest.status == 'Rejected', ServiceRequest.professional_id == professional_id).scalar() or 0)
    assigned = int(db.session.query(func.count(ServiceRequest.id)).filter(
                ServiceRequest.status == 'Assigned', ServiceRequest.professional_id == professional_id).scalar() or 0)
    closed = int(db.session.query(func.count(ServiceRequest.id)).filter(
                ServiceRequest.status.in_(['Paid', 'Closed']), ServiceRequest.professional_id == professional_id).scalar() or 0)

    return [requested, assigned, rejected, closed]









