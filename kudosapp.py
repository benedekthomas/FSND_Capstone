import os
import json
import sys

from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from database.models import db_drop_and_create_all, setup_db, Kudo, Team_Member

app = Flask(__name__)
try:
    setup_db(app)
    print('db setup worked')
except:
    print('db connection failed')
sys.stdout.flush()


@app.route("/check", methods=["GET"])
def health_check():
    return jsonify({
        "success": True,
        "message": "Server running"
    })


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)