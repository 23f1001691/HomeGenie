from flask_restful import Resource, reqparse, fields, marshal
from application.extensions import api, db
from application.models import Review
from application.utils import role_required
from flask_jwt_extended import jwt_required

review_parser = reqparse.RequestParser(bundle_errors=True)
review_parser.add_argument('id', type=int, help='Error: {error_msg}')
review_parser.add_argument('service_request_id', type=int, help='Error: {error_msg}')
review_parser.add_argument('feedback', type=str, help='Error: {error_msg}')
review_parser.add_argument('rating', type=int, help='Error: {error_msg}')

review_fields = {
    'id': fields.Integer,
    'service_request_id':fields.Integer,
    'feedback': fields.String,
    'rating': fields.Integer,
}
    
class ReviewAPI(Resource):      
    # @jwt_required()
    # @role_required(['customer'])
    def post(self):
        args = review_parser.parse_args(strict=True)
        new_review = Review(service_request_id=args['service_request_id'], 
                                             feedback=args['feedback'],
                                             rating=args['rating'])
        db.session.add(new_review)
        db.session.commit()

        return {"message":"Your review is updated."}, 201
 
api.add_resource(ReviewAPI, '/review')
