import json
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/status/live', methods=['GET'])
def get_live():
    return jsonify({"status":"ok"})
@app.route('/status/ready', methods=['GET'])
def get_ready():
    return jsonify({"status":"ok"})

app.run(port=8080)
