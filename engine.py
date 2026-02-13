from flask import Flask, render_template, redirect, request, session
from flask_socketio import SocketIO, send
from supabase import create_client
import os

# --- Supabase ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
password = os.getenv("PASSWORD")  # Mot de passe global
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Flask ---
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "une_cle_secrete_par_defaut")
socketio = SocketIO(app)

# --- Routes ---

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pseudo = request.form.get("pseudo")
        mdp = request.form.get("password")

        # Vérifie le mot de passe global
        if mdp == password and pseudo:
            session["pseudo"] = pseudo
            return redirect("/")
        else:
            return render_template("index.html", error="Pseudo ou mot de passe incorrect")

    return render_template("index.html")


@app.route("/")
def index():
    if "pseudo" not in session:
        return redirect("/login")
    return render_template("chat.html", pseudo=session["pseudo"])


# --- SocketIO ---

@socketio.on("message")
def handle_message(data):
    if "pseudo" not in data or "content" not in data:
        return

    # Enregistrer dans Supabase
    supabase.table("messages").insert({
        "pseudo": data["pseudo"],
        "content": data["content"]
    }).execute()

    # Envoyer à tous les clients
    send(data, broadcast=True)


# --- Lancement ---
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")
