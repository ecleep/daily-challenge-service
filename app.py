from flask import Flask, request, jsonify
import json

from db import init_db
from services import assign_challenge, complete_challenge, get_streak

HOST = "0.0.0.0"
PORT = 6000

app = Flask(__name__)
init_db()

with open("challenges.json", "r") as f:
    CHALLENGES = json.load(f)["categories"]


@app.route("/daily-challenge", methods=["GET"])
def daily_challenge():
    user_id = request.args.get("user_id")
    category = request.args.get("category", "general")

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    date, challenge = assign_challenge(user_id, category, CHALLENGES)

    return jsonify({
        "user_id": user_id,
        "category": category,
        "date": date,
        "challenge": challenge
    })


@app.route("/complete-challenge", methods=["POST"])
def complete():
    body = request.get_json()
    user_id = body.get("user_id")
    category = body.get("category", "general")

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    result = complete_challenge(user_id, category)

    if result is None:
        return jsonify({"error": "No challenge assigned today"}), 400

    count, date = result

    return jsonify({
        "message": "Challenge completed",
        "streak": count,
        "date": date
    })


@app.route("/streak", methods=["GET"])
def streak():
    user_id = request.args.get("user_id")

    return jsonify({
        "user_id": user_id,
        "streak": get_streak(user_id)
    })


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)