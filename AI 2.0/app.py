from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

FILE = "knowledge.json"


# Загружаем знания
if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        knowledge = json.load(f)
else:
    knowledge = {}


def save_knowledge():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, ensure_ascii=False, indent=4)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "error": "Вопрос пустой"
        })

    key = question.lower()

    # Если модель уже знает ответ
    if key in knowledge:
        return jsonify({
            "known": True,
            "answer": knowledge[key]
        })

    # Если вопрос неизвестен
    return jsonify({
        "known": False,
        "message": "Я пока не знаю ответа на этот вопрос."
    })


@app.route("/teach", methods=["POST"])
def teach():
    data = request.get_json()

    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()

    if not question or not answer:
        return jsonify({
            "error": "Вопрос или ответ пустой"
        })

    knowledge[question.lower()] = answer

    save_knowledge()

    return jsonify({
        "success": True,
        "message": "Я запомнила этот ответ!"
    })


if __name__ == "__main__":
    print("Модель запущена!")
    print("Открой в браузере: http://127.0.0.1:5000")

    app.run(debug=True)