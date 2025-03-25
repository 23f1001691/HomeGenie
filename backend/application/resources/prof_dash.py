from flask_restful import Resource
from application.extensions import api, db, cache
from application.models import Professional, User, Service, ServiceRequest, Payment
from flask import url_for
import os
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

        if professional.profile_pic and os.path.exists(professional.profile_pic):
            try:
                filename = os.path.basename(professional.profile_pic)
                professional.profile_pic = url_for('serve_profile', filename=filename, _external=True)
            except Exception as e:
                return {"message": f"Failed to retrieve the Profile: {str(e)}"}, 500
        else:
            professional.profile_pic = None

        print(professional.profile_pic)

        data1 = get_revenue_by_month(professional_id)

        return {
            "name": professional.name,
            "profile": professional.profile_pic,
            "description": professional.description,
            "service_name": professional.service_name,
            "rating": professional.rating,
            "data1": data1
        }, 200

api.add_resource(ProfDashAPI, '/prof-dash/<int:professional_id>')



def get_revenue_by_month(professional_id):
    revenue_data = (
        db.session.query(
            func.to_char(ServiceRequest.date_of_completion, 'FMMonth').label('month_name'),  # Get the month name
            func.sum(Payment.amount).label('total_revenue')
        )
        .join(Payment, Payment.service_request_id == ServiceRequest.id)
        .filter(ServiceRequest.professional_id == professional_id)
        .group_by(func.to_char(ServiceRequest.date_of_completion, 'FMMonth'))  # Group by month name
        .order_by('month_name')
        .all()
    )

    result = []
    for row in revenue_data:
        result.append({
            "month_name": row.month_name.strip(),
            "total_revenue": float(row.total_revenue) if row.total_revenue else 0.0
        })
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

    result = []
    for row in revenue_data:
        result.append({
            "month": row.month,
            "total_revenue": float(row.total_revenue) if row.total_revenue else 0.0
        })

    return result






