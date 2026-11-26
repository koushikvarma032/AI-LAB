import os
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    from routes.main_routes import main_bp
    from routes.diagnostic_routes import diagnostic_bp
    from routes.statistical_routes import statistical_bp
    from routes.bayesian_routes import bayesian_bp
    from routes.data_routes import data_bp
    from routes.report_routes import report_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(diagnostic_bp)
    app.register_blueprint(statistical_bp)
    app.register_blueprint(bayesian_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(report_bp)

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting AutoSense Nexus Web Application on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
