from flask import Flask
from application.config import DevelopmentConfig
from application.extensions import api, db, bcrypt, jwt, cors, mail, cache, init_excel
import application.resources.auth
from application.data import initialize_data

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

    with app.app_context():
        db.create_all()
        initialize_data()
        init_excel(app)

    return app
        
app = create_app()










