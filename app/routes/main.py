import os
from flask import Blueprint, render_template, current_app, session, redirect, url_for, flash, request, jsonify
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/voice-demo')
def voice_demo():
    demo_folder = current_app.config['DEMO_VOICE_FOLDER']
    voice_samples = [f for f in os.listdir(demo_folder) if f.endswith('.mp3')]
    return render_template('voice_demo.html', voice_samples=voice_samples)

@bp.route('/set-api-key', methods=['GET', 'POST'])
def set_api_key():
    if request.method == 'POST':
        api_key = request.form['api_key']
        session['api_key'] = api_key
        session['api_key_set_time'] = datetime.utcnow().timestamp()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"success": True, "message": "API key updated successfully"})
        
        flash('API key set successfully')
        return redirect(url_for('speech.speech_generator'))
    
    return render_template('set_api_key.html')