from flask import Flask
from . import auth, home

app = Flask(__name__)

app.register_blueprint(auth.bp)
app.register_blueprint(home.bp)

def start(env_vars:dict):
    app.secret_key = env_vars["SITE_SECRET_KEY"]
    app.run(host=env_vars["SITE_HOST"], port=env_vars["SITE_PORT"], debug=False)