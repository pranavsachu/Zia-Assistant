from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
from twilio.twiml.voice_response import VoiceResponse
from twilio_handler import handle_call_logic  # Placeholder for actual logic
from ai_engine import process_request  # Placeholder for AI engine logic
import database

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/call', methods=['POST'])
def handle_call_request():
    """Handle incoming calls from Twilio."""
    try:
        data = dict(request.form)
        logging.info(f"Incoming call data: {data}")
        user_input = None

        if "Digits" in data.keys():
            user_input = data['Digits']  # Captures user input from DTMF
            logging.info(f"Digits received: {user_input}")

        if not user_input:
            # Prompt user for input if no digits were received
            response = VoiceResponse()
            gather = response.gather(
                input="dtmf",
                num_digits=4,
                action="/call",
                method="POST"
            )
            gather.say("Hello, I am Zia AI Call Assistant for you . Please enter your passkey.")
            return str(response)

        # Process the user's input
        response = handle_call_logic(user_input,data['Caller'])
        
        return response
    except Exception as e:
        logging.error(f"Error handling call: {str(e)}")
        response = VoiceResponse()
        response.say(f"An error occurred: {str(e)}")
        return str(response), 500

@app.route('/message', methods=['POST'])
def handle_message_request():
    """Handle incoming messages from Twilio."""
    try:
        data = request.form
        logging.info(f"Incoming message data: {data}")

        user_input = data.get('Body')  # Message content
        user_phone = data.get('From')  # Sender's phone number

        if not user_input or not user_phone:
            return jsonify({'error': 'Invalid input or missing data'}), 400

        # Process the message using AI engine
        response = process_request(user_input, user_phone)
        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"Error handling message: {str(e)}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

@app.route('/', methods=['GET', 'POST'])
def add_user():
    """Render the form and handle form submission to insert user data."""
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name')
        phone = request.form.get('phone')
        passkey = request.form.get('passkey')
        age = request.form.get('age')
        blood_group = request.form.get('blood_group')
        cholesterol_level = request.form.get('cholesterol_level')
        sugar_level = request.form.get('sugar_level')
        accident_history = request.form.get('accident_history')
        surgery_history = request.form.get('surgery_history')

        # Insert the user into the database
        try:
            database.insert_user(
                name=name,
                phone=phone,
                passkey=passkey,
                age=int(age),
                blood_group=blood_group,
                cholesterol_level=float(cholesterol_level),
                sugar_level=float(sugar_level),
                accident_history=accident_history,
                surgery_history=surgery_history
            )
            return "User added successfully!"
        except Exception as e:
            logging.error(f"Error inserting user: {str(e)}")
            return f"An error occurred: {str(e)}", 500

    # Render the form
    return render_template('add_user.html')

@app.route('/', methods=['GET'])
def home():
    """Default route for health checks or status updates."""
    return "AI Call Assistant is running!"

if __name__ == '__main__':
    try:
        app.run(debug=True, host="0.0.0.0", port=5000)
    except Exception as e:
        logging.error(f"Error starting the Flask app: {str(e)}")



