import random
import datetime
from flask import Flask, flash, request, redirect, url_for, render_template

app = Flask(__name__)

def generate_rand(max):
    random.seed(datetime.datetime.now())
    return random.randint(1, max)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/1D4', methods=['GET', 'POST'])
def d4():
    result = generate_rand(4)
    return render_template("success.html", result=result)

@app.route('/1D6', methods=['GET', 'POST'])
def d6():
    result = generate_rand(6)
    return render_template("success.html", result=result)

@app.route('/1D8', methods=['GET', 'POST'])
def d8():
    result = generate_rand(8)
    return render_template("success.html", result=result)

@app.route('/1D20', methods=['GET', 'POST'])
def d20():
    result = generate_rand(20)
    return render_template("success.html", result=result)

@app.route('/1D100', methods=['GET', 'POST'])
def d100():
    result = generate_rand(100)
    return render_template("success.html", result=result)

if __name__ == '__main__':
    app.debug = True
    app.run()