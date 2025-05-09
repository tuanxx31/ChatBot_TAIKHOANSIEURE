from flask import Flask, request, jsonify
from database.chat_history_repository import ChatHistoryRepository
from database.connection import DBConnection
from services.strategies.role_based_strategy import RoleBasedStrategy
from services.strategies.description_strategy import DescriptionStrategy
from services.strategies.availability_strategy import AvailabilityStrategy
from nlp.entity_intent_analyzer import EntityIntentAnalyzer

app = Flask(__name__)

@app.route("/")
def index():
    return "Chatbot is running"

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    role = "customer"

    # analysis = EntityIntentAnalyzer().analyze(user_input)
    # intent = analysis["intent"]
    # product_name = analysis["product"]

    intent = "price"
    product_name = "capcut"

    if intent == "price":
        strategy = RoleBasedStrategy(role)
    elif intent == "description":
        strategy = DescriptionStrategy()
    elif intent == "availability":
        strategy = AvailabilityStrategy()
    else:
        return jsonify({"response": f"Chưa hỗ trợ intent '{intent}'"})

    response = strategy.handle(product_name)
    return jsonify({"response": response})



if __name__ == "__main__":
    app.run(debug=True)
 
