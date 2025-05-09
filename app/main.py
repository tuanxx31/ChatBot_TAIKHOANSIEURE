from flask import Flask, request, jsonify
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.chat_handler import ChatHandler

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

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    response = chat_handler.handle_message(user_input)
    return jsonify({"response": response})

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
 
