#!/usr/bin/env python3


import itertools
import random
from uuid import uuid4

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap


def generate_matches(options: list, n: int):
    options_len = len(options)
    pairs = options_len - 1

    total = sum([x for x in range(options_len)])
    if pairs > n:
        total = 1

    combos = [list(x) for x in list(itertools.product(options, options)) if x[0] != x[1]]
    sorted = []
    for x in combos:
        x.sort()
        if x not in sorted:
            sorted.append(x)
    combos = sorted * (total + 2)
    random.shuffle(combos)
    choices = {x: 0 for x in options}

    output = []  # bye
    for pair in combos:
        player0 = pair[0]
        player1 = pair[1]
        if choices.get(player0) < n and choices.get(player1) < n:
            output.append(pair)
            choices.update({player0: choices.get(player0) + 1, player1: choices.get(player1) + 1})
    for k, v in choices.items():
        if v < n:
            output.extend([[k, "**BYE**"]] * (n - v))

    output.sort()
    return output


app = Flask(__name__)
app.debug = True
app.secret_key = str(uuid4())
Bootstrap(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/match", methods=['POST'])
def match():
    rounds = request.form.get('rounds')
    players = request.form.get('players').replace("\r", "").split("\n")
    matches = generate_matches(players, int(rounds))
    return render_template("match.html", matches=matches)


app.run('0.0.0.0', 7878)
