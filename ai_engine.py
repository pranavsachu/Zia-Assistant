import database

def process_request(user_input, user_phone):
    # Example logic to handle messages
    if "appointment" in user_input.lower():
        appointment_id = database.insert_appointment_by_phone(user_phone)
        return f"Appointment booked successfully. Your ID is {appointment_id}."
    elif "history" in user_input.lower():
        user_data = database.get_user_data_by_phone(user_phone)
        if user_data:
            return f"Your medical history: {user_data}"
        else:
            return "No medical history found for your account."
    else:
        return "Sorry, I didn't understand your request. Please try again."
