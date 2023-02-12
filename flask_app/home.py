from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for


bp = Blueprint("home", __name__, url_prefix="/home")

@bp.route("/", methods=["GET"])
def home():
    return render_template("home/home.html")