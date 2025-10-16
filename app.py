# app.py - fix RCE
from flask import Flask, request, abort
import subprocess
import shlex

app = Flask(__name__)

@app.route('/')
def index():
    return "ok"

@app.route('/rce')
def rce():
    cmd = request.args.get('cmd')
    if not cmd:
        abort(400, "Missing cmd")
    # validation basique : autoriser uniquement des commandes whitelisted
    allowed = {"echo", "date"}
    parts = shlex.split(cmd)
    if parts[0] not in allowed:
        abort(403, "Commande non autorisée")
    # exécution sécurisée : liste d'arguments (pas d'interprétation shell)
    subprocess.run(parts, check=True)
    return "executed"
