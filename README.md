# FSND_Capstone
Capstone project in Udacity Fullstack Web Developer Nanodegree.


# Project Description
## Project Motivation
Kudos app aims to support the positive feedback, kudos culture in a team. It is a lightweight solution to collect and organiza all kudos given within a team.

## UI
In the scope of the project the focus lay on the backend, nevertheless to facilitate the login and API usage process a simple UI was created rendering only the '/' route.

The UI enables Login via Auth0, displays the Access JWT and the permissions assigned to the user.
The permissions are listed with the applicable endpoints as well.

## Roles and Permissions
The API handles 2 distinct roles:
- manager
- team-member

The manager role can administer the team-members in the database. Team-member users are not automatically registered in the database.

### Team member role
Team members have the permission to:
`<read:kudos>` read kudos either individual or multiples
`<create:kudos>` create persisten kudo addressed to an existing team member
`<get:team-members>` check the list of existing team members


### Manager Role
Managers have the permissions to:

```
get:kudos
create:kudos
get:team-members

patch:kudos
delete:kudos
create:team-member
delete:team-member
```

## API Architecture
1. POST /kudos/ 
  Record a new kudos

2. GET /kudos/ 
  Returns all kudos which are available to the visitor

3. GET /kudos/<kudos_id> 
  Returns a specific kudos with id <kudos_id>

4. PATCH /kudos/<kudos_id> 
  Updates the content of a specific kudos Returns the updated kudos

5. DELETE /kudos/<kudos_id> 
  Deletes a specific kudos Returns the id of the deleted kudos

6. GET /team-members/ 
  Returns a list of all team members

7. POST /team-members/ 
  Manager can add a team member.

8. DELETE /team-members/<team-member_id> 
  Delete a specific team member

9. GET /kudos/team-members/<team-member_id> 
  Returns all kudos given to a specific team member

## Database Schema
### Kudos
Representation of a feedback with the fields

```
id - unique id
text - String, literal description of the kudos
team_member_id - foreign key of the team member
date - date of entry in literal format
```

### Context
Representation of the context in which the feedback might be given.

```
team-member_id - id of the team member
name - name of the team member
position - position of the team member
```

