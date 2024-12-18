from database import session, User, set_passkey

# Create a user manually
new_user = User(
    name="thanguP",
    phone="+489944549",
    passkey=set_passkey("7931"),  # Hash the passkey before storing
    medical_history="kazhap."
)

# Add and commit the new user to the database
session.add(new_user)
session.commit()

print(f"User added with ID: {new_user.id}")
