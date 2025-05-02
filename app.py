from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

API_KEY = "sk-iUAXCawf3pmth203lEhJtw"
API_URL = "https://inference-api.nousresearch.com/v1/chat/completions"
MODEL = "DeepHermes-3-Mistral-24B-Preview"

SYSTEM_PROMPT = (
    "You are a deep thinking AI, you may use extremely long chains of thought to deeply "
    "consider the problem and deliberate with yourself via systematic reasoning processes "
    "to help come to a correct solution prior to answering. You should enclose your thoughts "
    "and internal monologue inside <think> </think> tags, and then provide your solution or response to the problem."
)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Chat</title>
</head>
<body style="font-family:sans-serif; max-width:600px; margin:auto; padding:2rem;">
    <h1>🧠 AI Chat</h1>
    <form method="post">
        <label>Запитайте у ШІ:</label><br><br>
        <textarea name="question" rows="4" cols="60">{{ question or '' }}</textarea><br><br>
        <button type="submit">Надіслати</button>
    </form>
    {% if answer %}
    <hr>
    <h3>🔽 Відповідь:</h3>
    <div style="white-space: pre-wrap;">{{ answer }}</div>
    {% endif %}
</body>
</html>
'''

def ask_ai(question):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": "Ask me anything, I am happy to help!"},
            {"role": "user", "content": question}
        ],
        "max_tokens": 256
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Помилка: {response.status_code}\n{response.text}"

@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    answer = ""
    if request.method == "POST":
        question = request.form.get("question", "")
        if question:
            answer = ask_ai(question)
    return render_template_string(HTML_TEMPLATE, question=question, answer=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
