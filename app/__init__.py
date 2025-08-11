from flask import Flask
from flask_migrate import Migrate
from config.config import Config
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from app.models.models import db
    db.init_app(app)
    
    migrate = Migrate(app, db)
    
    # Register template filter on app, not blueprint
    @app.template_filter('date')
    def format_date(value, format='%Y-%m-%d'):
        if isinstance(value, datetime):
            return value.strftime(format)
        return value
    
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp  
    from app.routes.donations import donations_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(donations_bp)
    
    return app
                    