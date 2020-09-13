from flask import Flask

import json

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "success": True,
        "message": "Server running"
    })

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)