import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.exceptions import abort

from Site.auth import login_required
from Site.db import get_db

bp = Blueprint("streamindex",__name__)

@bp.route("/")
def index():
    db = get_db()
    live_streams = get_live_streams()
    vods = db.execute(
        "SELECT * FROM vod"
        ).fetchall()
    return render_template("stream/index.html", live_streams=live_streams,vods=vods)

def get_live_streams():
    return []