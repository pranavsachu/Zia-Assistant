from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# OpenAI API key (replace with your own)
openai.api_key = "your-openai-api-key"

@app.route("/")
def home():
    """Render the chatbot UI."""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle user input and generate AI response."""
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Generate response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a health assistant AI."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
