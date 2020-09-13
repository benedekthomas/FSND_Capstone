import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "success": True,
        "message": "Server running"
    })


@app.route("/db", methods=["GET"])
def get_db_details():
    DATABASE_URL = os.environ['DATABASE_URL']
    return DATABASE_URL

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)