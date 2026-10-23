from flask import Flask, request, jsonify
from prometheus_client import Counter, generate_latest
from threading import Lock

app = Flask(__name__)
expenses = []
next_id = 1
lock = Lock()

REQUESTS = Counter(
    "expense_tracker_requests_total",
    "Total requests received by the application"
)

@app.before_request
def count_requests():
    REQUESTS.inc()

@app.route("/")
def home():
    return jsonify({"message": "Expense Tracker is running"})

@app.route("/expenses", methods=["GET"])
def get_expenses():
    with lock:
        return jsonify(expenses)

@app.route("/expenses", methods=["POST"])
def add_expense():
    global next_id
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    amount = data.get("amount")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    if (not isinstance(amount, (int, float))
            or isinstance(amount, bool)
            or amount <= 0):
        return jsonify({"error": "Amount must be positive"}), 400

    with lock:
        expense = {
            "id": next_id,
            "title": title.strip(),
            "amount": amount,
            "category": data.get("category", "General")
        }
        expenses.append(expense)
        next_id += 1

    return jsonify(expense), 201

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": "text/plain; version=0.0.4"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
