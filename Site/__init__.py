import os

from flask import Flask, g
from . import db, auth, streamindex, stream, restream


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY="dev",
            DATABASE=os.path.join(app.instance_path, "site.sqlite")
        )
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route("/siteisworking")
    def working():
        return "This is working"
    
    db.init_app(app)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(streamindex.bp)
    app.add_url_rule("/", endpoint="index")
    app.register_blueprint(stream.bp)
    app.register_blueprint(restream.bp)
    
    
    return app