import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from hashlib import md5


from Site.auth import login_required
from Site.db import get_db
import datetime
import random

bp = Blueprint("stream",__name__, url_prefix="/stream")

#@bp.route("/<id>")
def show_vod(id):
    db = get_db()
    vod = db.execute(
        "SELECT * FROM vod v JOIN user u ON v.author_id = u.id WHERE v.id = ? ",
        (id,)
        ).fetchone()
    if vod is not None:
        return render_template("stream/stream.html", vod=vod)
    else:
        flash("Oops, no vod was found at this location")
    return redirect(url_for("index"))

#@bp.route("/<url>")
def show_live(url):
    stream = find_live_stream_by_url(url)
    if stream is not None:
        return render_template("stream/stream.html", stream=stream)
    else:
        flash("Oops, the requested stream could not be found")
    return redirect(url_for("index"))

@bp.route("/golive", methods=("GET", "POST"))
def golive():
    if request.method == "POST":
        streamName = request.form["streamname"]
        password = request.form["password"]
        print("streamNamebefore "+streamName)
        if streamName is None or "" == streamName:
            streamName = "%032x" % random.getrandbits(128)
        print("streamNameAfter "+streamName)
        # start the streaming endpoint
        return redirect(url_for("stream.stream", inputUID=streamName))
    return render_template("stream/golive.html")

@bp.route("/<inputUID>")
def stream(inputUID):
    return render_template("stream/streaming.html",uid=inputUID)

@bp.route("/manage")
def manage():
    return "hullo"
        
        
        