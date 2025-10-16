# app.py (démo RCE)
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "ok"

@app.route('/rce')
def rce():
    cmd = request.args.get('cmd')        # <-- entrée utilisateur non filtrée
    os.system(cmd)                       # <-- vulnérabilité volontaire
    return "executed"
