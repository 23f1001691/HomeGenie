from flask_restful import Resource, reqparse, fields, marshal
from application.extensions import api, db, cache
from application.utils import role_required
from flask_jwt_extended import jwt_required
from flask import request
from application.models import Service, Professional, Category
from application.resources.prof import prof_resource_fields

service_resource_parser = reqparse.RequestParser()
service_resource_parser.add_argument('category_id', type=int)
service_resource_parser.add_argument('name', type=str)
service_resource_parser.add_argument('description', type=str)
service_resource_parser.add_argument('base_price', type=float)
service_resource_parser.add_argument('time_req', type=float)
service_resource_parser.add_argument('category', type=str)

service_resource_fields = {
    'id': fields.Integer,
    'category_id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'base_price': fields.Float,
    'time_req': fields.Float
}

class ServiceAPI(Resource):
    @jwt_required()
    @cache.cached(timeout = 5, key_prefix='service_data')
    def get(self, service_id):
        service = Service.query.get(service_id)
        if not service:
            return {"message": "Service_id not found"}, 404
        
        return marshal(service,service_resource_fields), 200

    @jwt_required()
    @role_required(["admin"])
    def put(self, service_id):
        args = service_resource_parser.parse_args()
        service = Service.query.get(service_id)
        if not service:
            return {"message":"ServiceID failed. Could not update the service."}, 404
        for key,value in args.items():
            if value is not None:
                setattr(service, key, value)
        if args["category"]:
            category = Category.query.filter_by(name=args["category"]).first()
            service.category_id = category.id
        db.session.commit()
        return {"message":"Service Updated"}, 200
        
    @jwt_required()
    @role_required(["admin"])
    def delete(self, service_id):
        service = Service.query.get(service_id)
        if not service:
            return {"message":"ServiceID not found. Could not delete the service."}, 404
        
        assigned = Professional.query.filter_by(service_id=service.id).first()
        if assigned:
            return {"message": "Cannot delete this service because it is assigned to one or more professionals."}, 400
        
        db.session.delete(service)
        db.session.commit()
        return {"message":"Service Deleted"}, 204    

class ServiceListAPI(Resource):
    @jwt_required()
    @role_required(["admin","customer"])
    @cache.cached(timeout = 5, key_prefix='service_list')
    def get(self):
        services = Service.query.all()
        if not services:
            return {"message":"No services available"},404 

        return marshal(services, service_resource_fields), 201

    @jwt_required()
    @role_required(["admin"])
    def post(self):
        args = service_resource_parser.parse_args(strict=True)
        print(args)
        service = Service.query.filter(Service.name == args["name"]).first()
        if service:
            return {"message":"Service already available"},404
        category = Category.query.filter_by(name=args["category"]).first()
        new_service = Service(name=args["name"], description=args["description"], base_price=args["base_price"],
                              time_req=args["time_req"], category_id=category.id)
        db.session.add(new_service)
        db.session.commit()
        return {"message":"Service Created"}, 201
    
api.add_resource(ServiceAPI, '/service/<int:service_id>')
api.add_resource(ServiceListAPI, '/services')

class FilterServicesAPI(Resource):
    @jwt_required()
    @role_required(["customer"])
    def get(self):

        filter_by = request.args.get('filter_by',None)
        search_query = request.args.get('search_query',None)
        
        services = Service.query.join(Professional, Service.id == Professional.service_id)
        
        if filter_by == 'Category' and search_query:
            category = Category.query.filter_by(name=search_query).first()
            services = services.filter(Service.category_id == category.id).all()
        elif filter_by == 'Service Name' and search_query:
            services = services.filter(Service.name.ilike(f'%{search_query}%')).all()
        elif filter_by == 'Pincode' and search_query:
            services = services.filter(Professional.pincode.ilike(f'%{search_query}%')).all()
        elif filter_by == 'Rating' and search_query:
            services = services.filter(Professional.rating >= float(search_query)).all()
        
        service_data = []

        for service in services:
            if len(service.professionals) > 0:
                professional_marshal = [marshal(prof, prof_resource_fields) for prof in service.professionals if prof.status == 'Approved' 
                                        and prof.flag == False and prof.user.is_profile_completed == True]
                service_marshal = marshal(service, service_resource_fields)
                service_marshal["professionals"] = professional_marshal
                if(service_marshal["professionals"]):
                    service_data.append(service_marshal)
                
        return service_data, 200

api.add_resource(FilterServicesAPI, '/filter-services') 

class viewServiceAPI(Resource):
    @jwt_required()
    @role_required(["customer"])
    def get(self, service_id, prof_id):
        service = Service.query.get(service_id)
        if not service:
            return {"message": "Service not found"}, 404

        professional = next((prof for prof in service.professionals if prof.id == prof_id), None)

        if not professional:
            return {"message": "Professional not found for the given service"}, 404

        service_marshal = marshal(service, service_resource_fields)
        service_marshal["professionals"] = dict(marshal(professional, prof_resource_fields))
                
        return service_marshal, 200

api.add_resource(viewServiceAPI, '/view-service/<int:service_id>/<int:prof_id>') 
