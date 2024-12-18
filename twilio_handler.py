from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
import database

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def handle_call_logic(user_input):
    """
    Handle incoming calls, verify the passkey, and respond with the user's medical history.

    Args:
        user_input (str): Passkey entered by the user.

    Returns:
        str: TwiML response to be sent back to Twilio.
    """
    response = VoiceResponse()
    try:
        # Fetch user data based on the provided passkey
        # user_data = get_user_data(user_input)
        user = database.get_user_data(user_input)
        if user:
            print("User ID:", user["id"])
            # Insert an appointment
            database.insert_appointment(user["id"], "Doctor visit", "2024-12-20")

            # Retrieve appointments for the user
            appointments = database.get_appointments_for_user(user["id"])
            print("Appointments:", appointments)
            print(f"user_data: {user}")
            #(name, phone, passkey, age, blood_group, cholesterol_level, sugar_level, accident_history, surgery_history)
            response.say(f"Hello {user['name']}. Here are your updated details: phone: {user['phone']}, age: {user['age']}, blood group: {user['blood_group']}, cholesterol level: {user['cholesterol_level']}, sugar level: {user['sugar_level']}, accident history: {user['accident_history']}, surgery history: {user['surgery_history']}")
        else:
            response.say("Invalid passkey. Please try again.")
    except Exception as e:
        response.say("An error occurred while processing your request. Please try again later.")
        print(f"Error in handle_call_logic: {e}")

    return str(response)

def send_message(to, message):
    """
    Send a message (SMS) to the specified phone number using Twilio.

    Args:
        to (str): The recipient's phone number.
        message (str): The message content.

    Returns:
        dict: The message status returned by Twilio.
    """
    try:
        sent_message = client.messages.create(
            to=to,
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )
        return {
            "status": "success",
            "sid": sent_message.sid,
            "message": "Message sent successfully."
        }
    except Exception as e:
        print(f"Error in send_message: {e}")
        return {
            "status": "failed",
            "error": str(e),
            "message": "Failed to send the message."
        }
