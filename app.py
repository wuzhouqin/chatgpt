import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        print(request.form)
        prompt = request.form["prompt"]
        print(prompt)
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     prompt=generate_prompt(animal),
        #     temperature=0.6,
        # )
        return redirect(url_for("index", result=prompt))

    result = request.args.get("result")
    return render_template("index.html", result=result)
