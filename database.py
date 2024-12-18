import sqlite3
from passlib.hash import bcrypt

# Database file
DATABASE_URL = "Zia.db"

# Connect to the database
def get_connection():
    """Establish and return a database connection."""
    return sqlite3.connect(DATABASE_URL)

# Create Tables
def create_tables():
    """Create 'users' and 'appointments' tables in the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                passkey TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                age INTEGER NOT NULL,
                blood_group TEXT NOT NULL,
                cholesterol_level FLOAT NOT NULL,
                sugar_level FLOAT NOT NULL,
                accident_history TEXT NOT NULL,
                surgery_history TEXT NOT NULL
            )
        ''')
        # Appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                details TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()

# Helper Functions
def set_passkey(raw_passkey):
    """Hash the passkey for secure storage."""
    return bcrypt.hash(raw_passkey)

def verify_passkey(raw_passkey, hashed_passkey):
    """Verify a raw passkey against the hashed passkey."""
    return bcrypt.verify(raw_passkey, hashed_passkey)

# User Operations
def get_user_by_passkey(passkey):
    """Retrieve a user by their passkey."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT id, name, phone, age, blood_group, cholesterol_level, sugar_level, accident_history, surgery_history FROM users WHERE passkey = ?", (passkey,))
            user = cursor.fetchone()
            if user:
                return {
                    "id": user[0],
                    "name": user[1],
                    "phone": user[2],
                    "age": user[3],
                    "blood_group": user[4],
                    "cholesterol_level": user[5],
                    "sugar_level": user[6],
                    "accident_history": user[7],
                    "surgery_history": user[8]
                }
            else:
                return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def insert_user(name, phone, passkey, age, blood_group, cholesterol_level, sugar_level, accident_history, surgery_history):
    """Insert a new user into the database."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, phone, passkey, age, blood_group, cholesterol_level, sugar_level, accident_history, surgery_history) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (name, phone, passkey, age, blood_group, cholesterol_level, sugar_level, accident_history, surgery_history)
            )
            conn.commit()
            print("User inserted successfully.")
    except sqlite3.IntegrityError as e:
        print("Error: Duplicate entry detected.")
    except Exception as e:
        print("An error occurred:", e)

def get_user_data(passkey):
    """Retrieve user data based on a valid passkey."""
    user_details = get_user_by_passkey(passkey)
    if user_details:
        print("User Details Found:")
        print(user_details)
        return user_details
    else:
        print("No user found with the provided passkey.")
        return None
    
def get_user_data_by_phone(phone):
    """Retrieve user data based on a valid phone number."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, phone, passkey, blood_group, cholesterol_level, sugar_level, accident_history, surgery_history FROM users WHERE phone = ?", (phone,))
            user = cursor.fetchone()
            if user:
                return {
                    "id": user[0],
                    "name": user[1],
                    "phone": user[2],
                    "passkey": user[3],
                    "blood_group": user[4],
                    "cholesterol_level": user[5],
                    "sugar_level": user[6],
                    "accident_history": user[7],
                    "surgery_history": user[8]
                }
            else:
                return None
    except Exception as e:
        print("An error occurred:", e)
        return None
    

# Appointment Operations
def insert_appointment(user_id, details, date):
    """Insert a new appointment for a user."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO appointments (user_id, details, date) VALUES (?, ?, ?)",
                (user_id, details, date)
            )
            conn.commit()
            print("Appointment inserted successfully.")
    except Exception as e:
        print("An error occurred:", e)

def insert_appointment_by_phone(phone, details, date):
    """Insert a new appointment for a user based on phone number."""
    try:
        user = get_user_data_by_phone(phone)
        if user:
            insert_appointment(user["id"], details, date)
        else:
            print("No user found with the provided phone number.")
    except Exception as e:
        print("An error occurred:", e)
        
def get_appointments_for_user(user_id):
    """Retrieve all appointments for a specific user."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, details, date FROM appointments WHERE user_id = ?", (user_id,))
            appointments = cursor.fetchall()
            return [{"id": row[0], "details": row[1], "date": row[2]} for row in appointments]
    except Exception as e:
        print("An error occurred:", e)
        return []

# Create tables when the script runs
# if __name__ == "__main__":
#     create_tables()
    
#     # Example usage
#     # Insert a new user
#     insert_user("John Doe", "+1 123 456 7890", "1234", 30, "O+", 200.5, 90.0, "No", "No")
#     insert_user("Jane Doe", "+1 987 654 3210", "4321", 28, "A-", 180.2, 85.5, "Yes", "No")
#     insert_user("Bob Smith", "+1 555 123 4567", "1111", 45, "B+", 220.7, 95.8, "No", "Yes")
    
    
#     # Retrieve user data
#     user = get_user_data("5678")
#     if user:
#         print("User ID:", user["id"])
#         # Insert an appointment
#         insert_appointment(user["id"], "Doctor visit", "2024-12-20")
        
#         # Retrieve appointments for the user
#         appointments = get_appointments_for_user(user["id"])
#         print("Appointments:", appointments)
