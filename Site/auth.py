import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash
from random import random, randint
from Site.db import get_db

bp = Blueprint("auth",__name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        
        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif db.execute(
            "SELECT id FROM user WHERE username = ?", (username,)
            ).fetchone() is not None:
            error = f"User {username} is already registered"
        
        if error:
            flash(error)
        else:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username,generate_password_hash(password))
                )
            db.commit()
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@bp.route("/login", methods=("GET","POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
            ).fetchone()
        
        if user is None:
            error = "Wrong username or password"
        elif not check_password_hash(user["password"], password):
            error = "Wrong username or password"
        
        if error:
            flash(error)
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
            ).fetchone()

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
            
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


'''
@bp.route("/rand0")
def rand0():
    return "you rolled a 0"

@bp.route("/rand1")
def rand1():
    return "you rolled a 1"

@bp.route("/rand2")
def rand2():
    return "you rolled a 2"

@bp.route("/surprise")
def randomTest():
    roll = randint(0,2)
    if 0 == roll:
        return redirect(url_for("auth.rand0"))
    elif 1 == roll:
        return redirect(url_for("auth.rand1"))
    elif 2 == roll:
        return redirect(url_for("auth.rand2"))
'''            