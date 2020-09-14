import os
import json
import sys

from flask import Flask, render_template, request, jsonify, abort
from sqlalchemy import exc
from database.models import db_drop_and_create_all, setup_db, Kudo, Team_Member

from auth.auth import AuthError, requires_auth

app = Flask(__name__)

# for logging, decide later what to do with this
try:
    setup_db(app)
    print('db setup worked')
except:
    print('db connection failed')
sys.stdout.flush()


# ROUTES
#  0 - not implemented,
#  1 - implemented, not tested
#  2 - implemented, tested in Postman

# (2) POST /kudos/ Record a new kudos
# (2) GET /kudos/ Returns all kudos which are available to the visitor
# (2) GET /kudos/<kudos_id> Returns a specific kudos with id <kudos_id>
# (2) PATCH /kudos/<kudos_id> Updates the content of a specific kudos
#       Returns the updated kudos
# (2) GET /team-members/ Returns a list of all team members
# (2) POST /team-members/ Manager can add a team member.
# (2) DELETE /team-members/<team-member_id>
#       Delete a specific team member with all kudos addressed to him/her
# (2) GET /kudos/team-members/<team-member_id> Returns
#       all kudos given to a specific team member


@app.route("/", methods=["GET"])
def index():
    AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
    AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
    API_AUDIENCE = os.environ['API_AUDIENCE']
    CALLBACK_URL = os.environ['CALLBACK_URL']

    data = {}
    link =  'https://' + \
            AUTH0_DOMAIN + '/authorize?' + \
            'audience=' + API_AUDIENCE + '&' + \
            'response_type=token&' + \
            'client_id=' + AUTH0_CLIENT_ID + '&' + \
            'redirect_uri=' + CALLBACK_URL
    data.update({'login_link': link})
    data.update({'host': CALLBACK_URL})

    endpoints = [
        {'permission':'create:kudos', 'endpoint': 'kudos', 'method': 'POST'},
        {'permission':'read:kudos', 'endpoint': 'kudos', 'method': 'GET'},
        {'permission':'read:kudos', 'endpoint': 'kudos/<kudo_id>', 'method': 'GET'},
        {'permission':'read:kudos', 'endpoint': 'kudos/team-members/<team-member_id>', 'method': 'GET'},
        {'permission':'patch:kudos', 'endpoint': 'kudos', 'method': 'PATCH'},
        {'permission':'delete:kudos', 'endpoint': 'kudos', 'method': 'DELETE'},
        {'permission':'get:team-members', 'endpoint': 'team-members', 'method': 'GET'},
        {'permission':'create:team-member', 'endpoint': 'team-members', 'method': 'POST'},
        {'permission':'delete:team-member', 'endpoint': 'team-members', 'method': 'DELETE'},
    ]
    data.update({'endpoints': endpoints})
    
    return render_template('pages/index.html', data = data)

# .............
# Kudo Endpoints
def check_team_member_id(team_member_id):
    """
    check_team_member_id
        helper function to identify valid team member ids
    """
    ids = set([team_member.id for team_member in Team_Member.query.all()])
    if not team_member_id in ids:
        return False
    return True

@app.route("/kudos", methods=["POST"])
@requires_auth("create:kudos")
def post_new_kudo(jwt):
    """
    POST /kudos
    """
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
                    "kudos": newKudo.long()
                    }), 201

@app.route("/kudos", methods=["GET"])
@requires_auth("read:kudos")
def get_kudos(jwt):
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

@app.route("/kudos/<int:kudo_id>", methods=["GET"])
@requires_auth("read:kudos")
def get_one_kudo(jwt, kudo_id):
    kudo = Kudo.query.filter_by(id=kudo_id).one_or_none()
    if kudo is None:
        abort(404)
    
    return jsonify({
                    "success": True,
                    "kudo": kudo.long()
                    })

@app.route("/kudos/<int:kudo_id>", methods=["PATCH"])
@requires_auth("patch:kudos")
def patch_one_kudo(jwt, kudo_id):
    kudo = Kudo.query.filter_by(id=kudo_id).one_or_none()
    if kudo is None:
        abort(404)
    
    newText = request.json.get("text", None)
    if newText is not None:
        kudo.text = newText
    
    newTeamMemberId = request.json.get("team_member_id", None)
    if newTeamMemberId is not None:
        kudo.team_member_id = newTeamMemberId

    newDate = request.json.get("date", None)
    if newDate is not None:
        kudo.date = newDate

    try:
        kudo.update()
    except exc.SQLAlchemyError:
        # return internal server error if couldn't add record
        abort(500)
    
    return jsonify({
                    "success": True,
                    "kudos": kudo.long()
                    })


# .............
# Team Member Endpoints
@app.route("/team-members", methods=["GET"])
@requires_auth("get:team-members")
def get_team_members(jwt):
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
                    "team-members": team_members
                    })

@app.route("/team-members", methods=["POST"])
@requires_auth("create:team-member")
def post_new_team_member(jwt):
    """
    POST endpoint
    record a new team member
    """
    newTeamMember = Team_Member(
        name=request.json.get("name", None),
        position=request.json.get("position", ""),
    )

    # name is a mandatory field, reject if missing
    if newTeamMember.name is None:
        abort(400)

    try:
        Team_Member.insert(newTeamMember)
    except exc.SQLAlchemyError:
        # return internal server error if couldn't add record
        abort(500)

    return jsonify({
                    "success": True,
                    "team-member": newTeamMember.display()
                    }), 201

@app.route("/team-members/<int:team_member_id>", methods=["DELETE"])
@requires_auth("delete:team-member")
def delete_team_member(jwt, team_member_id):
    team_member = Team_Member.query.filter_by(id = team_member_id).one_or_none()
    if team_member is not None:
        kudos = [kudo.short() for kudo in team_member.kudos]
    else:
        # abort for team members which are not in the DB
        abort(404)
    
    try:
        team_member.delete()
    except exc.SQLAlchemyError as error:
        abort(500)

    return jsonify({
                    "success": True,
                    "team-member": team_member.display(),
                    "kudos": kudos
                    })

@app.route("/kudos/team-members/<int:team_member_id>", methods=["GET"])
@requires_auth("read:kudos")
def get_all_kudos_of_a_team_member(jwt,team_member_id):
    team_member = Team_Member.query.filter_by(id=team_member_id).one_or_none()
    if team_member is None:
        abort(404)

    kudos = [kudo.short() for kudo in team_member.kudos]

    return jsonify({
                    "success": True,
                    "team-member": team_member.display(),
                    "kudos": kudos
                  })

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                    "success": False,
                    "error": error.status_code,
                    "message": error.error.get("description", "unknown error"),
                    }), error.status_code

if __name__ == '__main__':
    # Threaded option to enable multiple instances
    # for multiple user access support
    app.run(threaded=True, port=5000)
