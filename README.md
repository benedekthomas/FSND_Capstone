FSND_Capstone
Capstone project in Udacity Fullstack Web Developer Nanodegree.

Project Description
API Architecture
POST /kudos/ Record a new kudos

GET /kudos/ Returns all kudos which are available to the visitor

GET /kudos/<kudos_id> Returns a specific kudos with id <kudos_id>

PATCH /kudos/<kudos_id> Updates the content of a specific kudos Returns the updated kudos

DELETE /kudos/<kudos_id> Deletes a specific kudos Returns the id of the deleted kudos

GET /team-members/ Returns a list of all team members

POST /team-members/ Manager can add a team member.

DELETE /team-members/<team-member_id> Delete a specific team member

GET /kudos/team-members/<team-member_id> Returns all kudos given to a specific team member

Database Schema
Kudos
Representation of a feedback with the fields

kudos_id - unique id
kudos - String, literal description of the kudos
team-member - foreign key of the team member
date - timestamp
Context
Representation of the context in which the feedback might be given.

team-member_id - id of the team member
name - name of the team member
position - position of the team member
Roles and Permissions
Associate Role
Associates have the permission to:

get:kudos
create:kudos
get:team-members
Manager Role
Managers have the permissions to:

get:kudos
create:kudos
get:team-members

patch:kudos
delete:kudos
create:team-member
delete:team-member
