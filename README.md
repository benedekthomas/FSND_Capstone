# FSND_Capstone
Capstone project in Udacity Fullstack Web Developer Nanodegree.

# Project Description
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
kudos_id - unique id
kudos - String, literal description of the kudos
team-member - foreign key of the team member
date - timestamp
```

### Context
Representation of the context in which the feedback might be given.

```
team-member_id - id of the team member
name - name of the team member
position - position of the team member
```

## Roles and Permissions
### Team member role
team members have the permission to:
```
get:kudos
create:kudos
get:team-members
````

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
