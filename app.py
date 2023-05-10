import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        return redirect(url_for("index", result=prompt))

    result = request.args.get("result")
    return render_template("index.html", result=result)
