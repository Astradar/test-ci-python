# app.py - mini CTF vulnerable app (3 challenges)
from flask import Flask, request, render_template_string, send_from_directory, abort, Response
import sqlite3
import os
import subprocess

app = Flask(__name__)

# Flags (defaults, can be overridden by files in flags/)
FLAG_SQL = "FLAG{sql_injection_success}"
FLAG_UPLOAD = "FLAG{upload_shell_success}"
FLAG_RCE = "FLAG{rce_success}"

DB = 'ctf.db'
UPLOAD_DIR = 'uploads'
FLAGS_DIR = 'flags'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ------- DB init -------
def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        cur.execute("INSERT INTO users(username, password) VALUES('admin','s3cr3t')")
        conn.commit()
        conn.close()

init_db()

# Helper to optionally read external flags if present
def read_flag(path, default):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except Exception:
        return default

# expose flags from files if you put them in flags/
FLAG_SQL = read_flag(os.path.join(FLAGS_DIR, 'flag_sql.txt'), FLAG_SQL)
FLAG_UPLOAD = read_flag(os.path.join(FLAGS_DIR, 'flag_upload.txt'), FLAG_UPLOAD)
FLAG_RCE = read_flag(os.path.join(FLAGS_DIR, 'flag_rce.txt'), FLAG_RCE)

# ------- Home -------
@app.route('/')
def index():
    return """
    <h2>Mini-CTF demo</h2>
    <ul>
      <li><a href="/login">SQL Injection (web)</a></li>
      <li><a href="/upload">File Upload (web)</a></li>
      <li><a href="/ping">Command Injection (web)</a></li>
    </ul>
    <p>Environment: vuln app for training only. Do not expose publicly.</p>
    """

# ------- Challenge 1: SQLi -------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user','')
        pw = request.form.get('pass','')
        # vulnerable query (intended)
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        q = f"SELECT * FROM users WHERE username='{user}' AND password='{pw}'"
        try:
            cur.execute(q)
            row = cur.fetchone()
        except Exception:
            row = None
        conn.close()
        if row:
            return f"<h3>Bienvenue {user}!</h3><p>FLAG: <b>{FLAG_SQL}</b></p>"
        else:
            return "<p>Identifiants invalides.</p>"
    return """
    <h3>Login (challenge SQLi)</h3>
    <form method='post'>
      <input name='user' placeholder='user'><br>
      <input name='pass' placeholder='pass'><br>
      <button type='submit'>Login</button>
    </form>
    <p>Indice: essaye d'injecter dans les champs (ex: ' OR 1=1 -- )</p>
    """

# ------- Challenge 2: File upload -------
ALLOWED_EXT = ['jpg','png','txt']  # intentionally weak / illustrative
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        if not f:
            return "No file"
        filename = f.filename
        # insecure: no proper validation, move file as-is
        dest = os.path.join(UPLOAD_DIR, filename)
        f.save(dest)
        return f"Upload réussi: <a href='/uploads/{filename}' target='_blank'>{filename}</a><br>"
    return """
    <h3>Upload challenge</h3>
    <form method='post' enctype='multipart/form-data'>
      <input type='file' name='file'><br>
      <button type='submit'>Upload</button>
    </form>
    <p>Indice: renomme un fichier ex: reveal_flag.txt et tente d'y accéder via le lien retourné.</p>
    """

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    # special behavior for CTF upload challenge:
    # if the uploaded filename is exactly 'reveal_flag.txt', return the flag content
    if filename == "reveal_flag.txt":
        flag_path = os.path.join(FLAGS_DIR, "flag_upload.txt")
        try:
            with open(flag_path, "r") as f:
                data = f.read()
            return Response(data + "\n", mimetype="text/plain")
        except Exception as e:
            return f"Erreur lecture flag: {e}", 500

    # default behavior: serve the file as-is (no security) - intended for lab only
    return send_from_directory(UPLOAD_DIR, filename)

# ------- Challenge 3: Command injection -------
@app.route('/ping')
def ping():
    ip = request.args.get('ip','127.0.0.1')
    # vulnerable concatenation (intended)
    try:
        output = subprocess.check_output(f"ping -c 1 {ip}", shell=True, stderr=subprocess.STDOUT, timeout=5)
        return f"<pre>{output.decode(errors='ignore')}</pre>"
    except Exception as e:
        return f"Erreur: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
