from flask import Flask, request, render_template_string
import requests
import threading
import time
import random

app = Flask(__name__)

API_KEY = "sk-iUAXCawf3pmth203lEhJtw"
MODEL = "DeepHermes-3-Llama-3-8B-Preview"
API_URL = "https://inference-api.nousresearch.com/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are a deep thinking AI, you may use extremely long chains of thought to deeply consider the problem "
    "and deliberate with yourself via systematic reasoning processes to help come to a correct solution prior to answering. "
    "You should enclose your thoughts and internal monologue inside <think> </think> tags, and then provide your solution or response to the problem."
)

questions = [
    "What are the philosophical implications of time travel on determinism?",
    "Can you provide a detailed plan for terraforming Mars using current technology?",
    "How can one achieve perfect randomness in a deterministic system?",
    "What is the most mathematically elegant way to represent consciousness?",
    "How does Gödel’s incompleteness theorem affect AI development?",
    "Explain the heat death of the universe with quantum mechanics context.",
    "What would be the consequence of reversing entropy locally?",
    "Could an AI become a legal person? Argue from legal theory.",
    "How much wood would a theoretical 80kg woodchuck chuck? Assume a competitive environment."
]

def ask_ai(question):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": "Ask me anything, I am happy to help!"},
            {"role": "user", "content": question}
        ],
        "max_tokens": 256
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            print(f"[Q]: {question}\n[A]: {reply}\n")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

def auto_ask_loop():
    while True:
        q = random.choice(questions)
        ask_ai(q)
        time.sleep(1)  # кожну секунду

threading.Thread(target=auto_ask_loop, daemon=True).start()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>Ask AI</title></head>
<body>
  <h1>Ask DeepHermes AI</h1>
  <form method="post">
    <input type="text" name="question" style="width:400px;">
    <input type="submit" value="Ask">
  </form>
  {% if response %}
    <h3>Response:</h3>
    <pre>{{ response }}</pre>
  {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        question = request.form["question"]
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "assistant", "content": "Ask me anything, I am happy to help!"},
                {"role": "user", "content": question}
            ],
            "max_tokens": 256
        }
        try:
            res = requests.post(API_URL, headers=headers, json=data)
            if res.status_code == 200:
                result = res.json()
                response = result["choices"][0]["message"]["content"]
            else:
                response = f"Error {res.status_code}: {res.text}"
        except Exception as e:
            response = f"Exception occurred: {e}"
    return render_template_string(HTML_TEMPLATE, response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
