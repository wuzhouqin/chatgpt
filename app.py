import os
import openai
from flask import Flask, redirect, render_template, request, url_for, jsonify

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

conversation = [
    {"role":"system", "content": "你是一个理智而幽默的的个人助理"},
]

def clear_conversation():
    conversation = [
        {"role":"system", "content": "你是一个理智而幽默的的个人助理"},
    ]

@app.route("/dingtalk", methods=["POST"])
def dingtalk():
    print(request.json)
    msg = request.json;
    if msg["msgtype"] == "text":
        content = msg["text"]["content"]
        if content == "新会话":
            clear_conversation()
            data["msgtype"] = "text"
            text = {}
            text["content"] = "好的"
            data["text"] = text
            return jsonify(data)
        else:
            conversation.append({"role":"user", "content":"{}".format(content)})
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages = conversation,
                temperature=0.6,
            )
            answer = response.choices[0].message.content
            conversation.append({"role":"assistant", "content":"{}".format(answer)})
            data["msgtype"] = "text"
            text = {}
            text["content"] = answer
            data["text"] = text
            return jsonify(data)

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        print(prompt)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages = [
                {"role":"system", "content": "你是一个理智而幽默的的个人助理"},
                {"role":"user", "content":"{}".format(prompt)},
            ],
            temperature=0.6,
        )
        print(response)
        return render_template("index.html", result=response.choices[0].message.content)

    result = request.args.get("result")
    return render_template("index.html", result=result)
