import os
import json
import sys

from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from database.models import db_drop_and_create_all, setup_db, Kudo, Team_Member

app = Flask(__name__)

# for logging, decide later what to do with this
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


@app.route("/team-members", methods=["GET"])
def get_team_members():
    """
    GET endpoint
    returns all team members as a list of dicts
    team members are in display() format
    """
    try:
        team_members = [team_member.display() for team_member in Team_Member.query.all()]
    except exc.SQLAlchemyError:
        # return internal server error if couldn't add record
        abort(500)

    return jsonify({
                    "success": True,
                    "team_members": team_members
                    })

@app.route("/team-members", methods=["POST"])
def post_new_team_member():
    """
    POST endpoint
    record a new team member
    """
    newTeamMember = Team_Member(
        name=request.json.get("name", "default=Missing name"),
        position=request.json.get("position", ""),
    )

    try:
        Team_Member.insert(newTeamMember)
    except exc.SQLAlchemyError:
        # return internal server error if couldn't add record
        abort(500)

    return jsonify({
                    "success": True,
                    "team-member": newTeamMember.display()
                    }) 


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)