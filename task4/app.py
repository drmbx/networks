import flask
from flask import Flask, request
import parser

app = Flask(__name__)


@app.route("/parse", methods=['GET'])
def parse():
    url = request.args.get("url")
    if not url:
        return flask.jsonify({'error': 'Missing url parameter'}), 400

    return parser.parse(url)


if __name__ == '__main__':
    app.run()
