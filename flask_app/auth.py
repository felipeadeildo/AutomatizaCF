from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from database.utils import MySQL

bp = Blueprint('auth', __name__, url_prefix='/')
conn = MySQL()

@bp.route('/sigin', methods = ["GET", "POST"])
def sigin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        has_user = conn.execute("SELECT password, role, permission_level FROM workspace_users WHERE username = %s", (username, )).fetchone()
        status = None
        if has_user is None:
            status = "Usuário e/ou senha incorretos"
        else:
            if password == has_user[0]:
                session.clear()
                session["username"] = username
                session["role"] = has_user[1]
                session["permission_level"] = has_user[2]
                status = "Logado com sucesso"
                return redirect(url_for('home.home'))
            else:
                status = "Usuário e/ou senha incorretos"
        flash(status)
    return render_template("auth/sigin.html")