import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
import os

from Site.auth import login_required
from Site.db import get_db
from werkzeug import Response, Request
from sys import byteorder

bp = Blueprint("restream",__name__, url_prefix="/show")
base = "/home/finnk/Programming/Projects/python/Streaming Server Frontend"
archiveLocation = "/archive"
liveLocation = "/live"

@bp.route("/receive/<uid>", methods=("POST",))
def receive(uid):
    chunkNumber = get_chunk_number(uid) #number of the current incoming chunck
    filepath = base+liveLocation+f"/{uid}" 
    filename= f"/{chunkNumber}.webm"
    
    stream = request.data
    with open(filepath+filename, "wb") as out:
        out.write(stream)
        out.close()
    
    return "OK"
    
def get_chunk_number(uid):
    filepath = base+liveLocation+f"/{uid}"
    if not os.path.isdir(filepath):
        os.makedirs(filepath, exist_ok=True)   
    chunknumber = 0
    if os.path.isfile(filepath+"/chunk"):
        with open(filepath+"/chunk", "rb") as read:
            bytes = read.read(4)
            chunknumber+=int.from_bytes(bytes, byteorder="little")
            chunknumber+=1
            read.close()
    with open(filepath+"/chunk", "wb") as out:
        out.write((chunknumber).to_bytes(4, byteorder="little"))
        out.close()
    return chunknumber
        
        
@bp.route("/<uid>")
def show(uid):
    live = uid in g.streamsLife
    if live:
        if not os.path.isdir(base+liveLocation+f"/{uid}"):
            flash("oops, this stream is not available")
            return redirect("index")
        chunk = g.streamsLife[uid]
        return render_Template("show.html", src=base+liveLocation+f"/{uid}", start=chunk)
    else:
        if not os.path.isdir(base+archiveLocation+f"/{uid}"):
            flash("oops, this stream is not available")
            return redirect("index")
        return render_template("show.html",src=base+archiveLocation+f"/{uid}")
    