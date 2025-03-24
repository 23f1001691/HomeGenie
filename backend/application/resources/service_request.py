from flask_restful import Resource, reqparse, fields, marshal
from application.extensions import api, db, cache
from application.models import ServiceRequest, User, Professional
from datetime import datetime
from application.utils import role_required, format_date
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from sqlalchemy import or_
import json

DATE_FORMAT = '%Y-%m-%d'

service_request_parser = reqparse.RequestParser(bundle_errors=True)
service_request_parser.add_argument('id', type=int, help='Error: {error_msg}')
service_request_parser.add_argument('service_id', type=int, help='Error: {error_msg}')
service_request_parser.add_argument('customer_id', type=int, help='Error: {error_msg}')
service_request_parser.add_argument('professional_id', type=int, help='Error: {error_msg}')
service_request_parser.add_argument('date_of_request', 
                                    type=lambda x: datetime.strptime(x, DATE_FORMAT).date() if x else None,
                                    help='Error: {error_msg}')
service_request_parser.add_argument('date_of_completion', 
                                    type=lambda x: datetime.strptime(x, DATE_FORMAT).date() if x else None,
                                    help='Error: {error_msg}')
service_request_parser.add_argument('status_updated_by', type=str, help='Error: {error_msg}')
service_request_parser.add_argument('status', type=str, help='Error: {error_msg}')

service_request_fields = {
    'id': fields.Integer,
    'service_id':fields.Integer,
    'customer_id': fields.Integer,
    'professional_id': fields.Integer,
    'date_of_request': fields.String(attribute=lambda x: format_date(x.date_of_request)),
    'date_of_completion': fields.String(attribute=lambda x: format_date(x.date_of_completion)),
    'status_updated_by': fields.String,
    'status': fields.String,
}

class ServiceRequestAPI(Resource):
    @jwt_required()
    @cache.cached(timeout = 5, key_prefix='service_request_data')
    def get(self, service_request_id):
        service_request = ServiceRequest.query.get(service_request_id)
        if not service_request:
            return {"message":"ServiceRequestID not found"}, 404
        
        return marshal(service_request,service_request_fields), 201
    
    @jwt_required()
    @role_required(['customer','professional'])
    def put(self, service_request_id):
        args = service_request_parser.parse_args(strict=True)
        service_request = ServiceRequest.query.get(service_request_id)

        if not service_request:
            return {"message":"ServiceRequestID not found"}, 404
        
        original_status = service_request.status
        
        if ('customer_id' in args) and (args['customer_id'] is not None):
            return {"message": "customerID cannot be changed after creation"}, 403
                
        for key,value in args.items():
            if value is not None:
                setattr(service_request, key, value)  
                
        db.session.commit()

        if original_status != service_request.status and (service_request.status == 'Assigned' or service_request.status == 'Rejected'):
            pass
            # Send mail to the customer saying whether request is accepted or rejected
            #Add in future

        return {"message":"Service_request updated"}
    
    @jwt_required()
    @role_required(['customer'])
    def delete(self, service_request_id):
        service_request = ServiceRequest.query.get(service_request_id)

        if not service_request:
            return {"message":"ServiceRequestID not found. Could not delete the service request."}, 404
        
        if service_request.status != 'Requested':
            return {"message": "Cannot delete this service request as your request is accepted by the professional."}, 400
        
        db.session.delete(service_request)
        db.session.commit()
        return {"message":"Service Request Deleted"}, 204   
    
class ServiceRequestListAPI(Resource):
    @jwt_required()
    @role_required(['admin'])
    @cache.cached(timeout = 5, key_prefix='service_request_list')
    def get(self):
        service_requests = ServiceRequest.query.all()
        if not service_requests:
            return {"message":"No service requests available"},404
        return marshal(service_requests, service_request_fields), 201            

    @jwt_required()
    @role_required(['customer'])
    def post(self):
        args = service_request_parser.parse_args(strict=True)
        user = User.query.get(args['customer_id'])
        if not user:
            return {"message":"Unregistered userID"}, 404
        customer = user.customer
        new_service_request = ServiceRequest(service_id=args['service_id'], 
                                             professional_id=args['professional_id'],
                                             customer_id=customer.id)
        db.session.add(new_service_request)
        db.session.commit()

        return {"message":"Your service request is sent. Wait for sometime. Professional will get back to you soon."}, 201
 
api.add_resource(ServiceRequestListAPI, '/service-requests')
api.add_resource(ServiceRequestAPI, '/service-request/<int:service_request_id>')