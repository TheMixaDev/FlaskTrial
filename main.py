from flask import Flask

from blueprints.json_route import json_blueprint
from blueprints.xml_route import xml_blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(json_blueprint)
app.register_blueprint(xml_blueprint)


@app.route("/")
def hello_world():
    return "Root route"


if __name__ == "__main__":
    app.run(debug=False)
