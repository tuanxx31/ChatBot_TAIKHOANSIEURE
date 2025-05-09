from flask import Flask, request, jsonify
from services.chat_handler import ChatHandler

app = Flask(__name__)
chat_handler = ChatHandler()

@app.route("/")
def index():
    return "Chatbot is running"

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
        
    response = chat_handler.handle_message(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
 
