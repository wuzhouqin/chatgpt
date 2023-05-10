import os
import openai
import requests
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
    data = {}
    text = {}
    data["msgtype"] = "text"
    data["text"] = text
    
    if msg["msgtype"] == "text":
        content = msg["text"]["content"]
        sessionWebhook = msg["sessionWebhook"]
        if content == "新会话":
            clear_conversation()
            text["content"] = "好的"
        else:
            conversation.append({"role":"user", "content":"{}".format(content)})
            print(conversation)
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages = conversation,
                temperature=0.6,
            )
            print(response)
            answer = response.choices[0].message.content
            print(answer)
            conversation.append({"role":"assistant", "content":"{}".format(answer)})
            text["content"] = answer
        requests.post(sessionWebhook, json=data)
        return jsonify({})
    else:
        text["content"] = "不支持回复此消息"
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
