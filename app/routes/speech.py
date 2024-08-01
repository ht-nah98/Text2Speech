from flask import Blueprint, render_template, request, send_file, session, redirect, url_for, flash, jsonify
from app.utils.speech_generator import generate_speech
from app.utils.auth import is_api_key_valid
import os

bp = Blueprint('speech', __name__, url_prefix='/speech')

@bp.route('/generator', methods=['GET', 'POST'])
def speech_generator():
    if not is_api_key_valid():
        flash('Your API key has expired or is not set. Please enter it again.')
        return redirect(url_for('main.set_api_key'))
    
    if request.method == 'POST':
        text = request.form['text']
        voice = request.form['voice']
        speed_factor = float(request.form['speed_factor'])
        
        try:
            output_filename = generate_speech(text, voice, speed_factor, session['api_key'])
            
            # Send the file and then delete it
            return_value = send_file(output_filename, mimetype='audio/mpeg', as_attachment=True)
            os.remove(output_filename)  # Delete the file after sending
            
            return return_value
        except Exception as e:
            error_message = str(e)
            if "Invalid API key" in error_message:
                session.pop('api_key', None)
                session.pop('api_key_set_time', None)
                return jsonify({"error": "Invalid API key. Please enter a new one."}), 401
            return jsonify({"error": f"Error generating speech: {error_message}"}), 500
    
    return render_template('speech_generator.html')