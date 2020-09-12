import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Kudo, Team_Member
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

# ROUTES
#  0 - not implemented,
#  1 - implemented, not tested
#  2 - implemented, tested in Postman
#  3 - implmeneted, tested with Pytest

# (2) POST /kudos/ Record a new kudos
# (1) GET /kudos/ Returns all kudos which are available to the visitor
# ( ) GET /kudos/<kudos_id> Returns a specific kudos with id <kudos_id>
# ( ) PATCH /kudos/<kudos_id> Updates the content of a specific kudos Returns the updated kudos
# ( ) DELETE /kudos/<kudos_id> Deletes a specific kudos Returns the id of the deleted kudos
# (2) GET /team-members/ Returns a list of all team members
# (2) POST /team-members/ Manager can add a team member.
# (?) DELETE /team-members/<team-member_id> Delete a specific team member
# ( ) GET /kudos/team-members/<team-member_id> Returns all kudos given to a specific team member

def check_team_member_id(team_member_id):
    """
    check_team_member_id
        helper function to identify valid team member ids
    """
    ids = set([team_member.id for team_member in Team_Member.query.all()])
    if not team_member_id in ids:
        return False
    return True

@app.route("/kudos", methods=["GET"])
def get_kudos():
    """
    Returns all kudos which are available to the visitor  
    """
    try:
        kudos = [kudo.short() for kudo in Kudo.query.all()]
    except exc.SQLAlchemyError:
        # return internal server error if couldn't add record
        abort(500)

    return jsonify({
                    "success": True,
                    "kudos": kudos
                    })


"""
POST /kudos
"""
@app.route("/kudos", methods=["POST"])
def post_new_kudo():
    newKudo = Kudo(
        text=request.json.get("text", "default=You are Great!"),
        team_member_id=request.json.get("team_member_id", 1),
        date=request.json.get("date", "2020-01-01"),
    )
    if not check_team_member_id(newKudo.team_member_id):
        # abort with bad request
        abort(400)
    try:
        Kudo.insert(newKudo)
    except exc.SQLAlchemyError:
        # return internal server error if couldn't add record
        abort(500)

    return jsonify({
                    "success": True,
                    "kudos": newKudo.short()
                    })

# ######## TEAM MEMBER ENDPOINTS ########
@app.route("/team-members", methods=["GET"])
def get_team_members():
    """
    GET endpoint
    returns all team members as a list of dicts
    team members are in display() format
    """
    try:
        team_members = [team_member.display() for team_member in Team_Member.query.all()]
    except exc.SQLAlchemyError as error:
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

# Deleting a team member raises errors due the kudos remaining in the DB and ids are being nulled.
# @app.route("/team-members/<int:team_member_id>", methods=["DELETE"])
# def delete_team_member(team_member_id):
#     team_member = Team_Member.query.filter_by(id = team_member_id).one_or_none()

#     # abort for team members which are not in the DB
#     if team_member == None:
#         abort(404)
#     try:
#         team_member.delete()
#     except exc.SQLAlchemyError as error:
#         abort(500)

#     return jsonify({
#                     "success": True,
#                     "deleted": team_member.display()
#                     })



# """
# POST /drinks
#     it should create a new row in the drinks table
#     it should require the 'post:drinks' permission
#     it should contain the drink.long() data representation
# returns status code 200 and json {"success": True, "drinks": drink} where
#     drink an array containing only the newly created drink
#     or appropriate status code indicating reason for failure
# """


# @app.route("/drinks", methods=["POST"])
# # @requires_auth("post:drinks")
# def create_new_drink(jwt):
#     newDrink = Drink(
#         title=request.json.get("title", ""),
#         recipe=json.dumps(request.json.get("recipe", "")),
#     )

#     try:
#         Drink.insert(newDrink)
#     except exc.SQLAlchemyError:
#         # return internal server error if couldn't add record
#         abort(500)

#     return jsonify({
#                     "success": True,
#                     "drinks": [newDrink.long()]
#                     })


# """
# PATCH /drinks/<int:drink_id>
#     where <drink_id> is the existing model id
#     it should respond with a 404 error if <id> is not found
#     it should update the corresponding row for <id>
#     it should require the 'patch:drinks' permission
#     it should contain the drink.long() data representation
# returns status code 200 and json {"success": True, "drinks": drink} where
#     drink an array containing only the updated drink
#     or appropriate status code indicating reason for failure
# """


# @app.route("/drinks/<int:drink_id>", methods=["PATCH"])
# # @requires_auth("patch:drinks")
# def patch_drink(jwt, drink_id):
#     drink = Drink.query.filter_by(id=drink_id).one_or_none()
#     if drink is None:
#         # Drink with ID is not found
#         return jsonify({
#                         "success": False,
#                         "error": 404,
#                         "message": ("Drink #{} not found.".format(drink_id))
#                         }), 404

#     if request.json.get("title", "") != "":
#         drink.title = request.json.get("title", "")

#     if request.json.get("recipe", "") != "":
#         drink.recipe = json.dumps(request.json.get("recipe", ""))

#     return jsonify({
#                     "success": True,
#                     "drinks": [drink.long()]
#                     })


# """
# DELETE /drinks/<int:drink_id> endpoint
#     where <drink_id> is the existing model id
#     it should respond with a 404 error if <drink_id> is not found
#     it should delete the corresponding row for <id>
#     it should require the 'delete:drinks' permission
# returns status code 200 and json {"success": True, "delete": id} where id is
#     the id of the deleted record
#     or appropriate status code indicating reason for failure
# """


# @app.route("/drinks/<int:drink_id>", methods=["DELETE"])
# # @requires_auth("delete:drinks")
# def delete_drink(jwt, drink_id):
#     drink = Drink.query.filter_by(id=drink_id).one_or_none()

#     if drink is None:
#         # Drink with ID is not found
#         return jsonify({
#                         "success": False,
#                         "error": 404,
#                         "message": ("Drink #{} not found.".format(drink_id))
#         }), 404

#     try:
#         drink.delete()
#     except exc.SQLAlchemyError:
#         # return internal server error if couldn't delete record
#         abort(500)

#     return jsonify({"success": True, "delete": drink_id})


# Error Handling
"""
HTTP error handlers> 400, 404, 422, 500
"""


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "bad request"
                    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
                }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
                    "success": False,
                    "error": 500,
                    "message": "Internal server error",
                    }), 500


"""
Authentication error handlers
"""


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                    "success": False,
                    "error": error.status_code,
                    "message": error.error.get("description", "unknown error"),
                    }), error.status_code
                   