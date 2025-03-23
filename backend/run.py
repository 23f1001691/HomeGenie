from application import app
from application.celery.celery_factory import celery_init_app

celery = celery_init_app(app)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)