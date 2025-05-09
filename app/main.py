from flask import Flask, request, jsonify
from database.chat_history_repository import ChatHistoryRepository
from database.connection import DBConnection
from services.strategies.role_based_strategy import RoleBasedStrategy
from nlp.intent_classifier import IntentClassifier
from services.strategies.description_strategy import DescriptionStrategy
from services.strategies.availability_strategy import AvailabilityStrategy

app = Flask(__name__)

@app.route("/")
def index():
    return "Chatbot is running"

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    role = "ctv"  # hiện tại fix cứng, sau này sẽ lấy từ token

    # Dùng GPT phân tích intent
    intent = IntentClassifier().classify(user_input)

    # Mapping intent sang Strategy
    if intent == "price":
        strategy = RoleBasedStrategy(role)
    elif intent == "description":
        strategy = DescriptionStrategy()
    elif intent == "availability":
        strategy = AvailabilityStrategy()
    else:
        return jsonify({"response": f"Chưa hỗ trợ intent '{intent}'"})

    # Gọi strategy phù hợp
    response = strategy.handle(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
 
