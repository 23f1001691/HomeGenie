from flask import Flask
from application.config import DevelopmentConfig
from application.extensions import api, db, bcrypt, jwt, cors, mail, cache, init_excel
import application.resources.category
import application.resources.prof
import application.resources.customer
import application.resources.service
from application.data import initialize_data
from flask_jwt_extended import get_jwt
from application.models import User

def create_app():
    app = Flask(__name__)

    #Configuring app before initialisation
    app.config.from_object(DevelopmentConfig)

    #Initialising extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    bcrypt.init_app(app)
    api.init_app(app)
    cors.init_app(app, expose_headers=["Authorization","X-CSRF-TOKEN"], resources={r"/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)

    app.app_context().push()

    @jwt.user_identity_loader
    def user_identity_lookup(id):
        return str(id)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        user = User.query.get(identity) 
        if user:
            return {
                "role": user.role
            }
        return {}

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        print(identity)
        return User.query.filter_by(id=identity).one_or_none()

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            return response

    with app.app_context():
        db.create_all()
        initialize_data()
        init_excel(app)
        # import application.auth 

    return app
        
app = create_app()

from application.auth import *
from application.routes import *
from application.admin import *










