from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/status/live', methods=['GET'])
def get_live():
    return jsonify({"status": "ok"})


@app.route('/status/ready', methods=['GET'])
def get_ready():
    return jsonify({"status": "ok"})


app.run(host='0.0.0.0', debug=False, port=8080)
