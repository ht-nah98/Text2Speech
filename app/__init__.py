from flask import Flask, send_from_directory
from config import Config
from flask_session import Session

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    from app.routes import main, speech
    app.register_blueprint(main.bp)
    app.register_blueprint(speech.bp)

    @app.route('/static/demo_voice/<path:filename>')
    def serve_audio(filename):
        return send_from_directory(app.config['DEMO_VOICE_FOLDER'], filename, mimetype='audio/mpeg')

    return app