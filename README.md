# FSND_Capstone
Capstone project in Udacity Fullstack Web Developer Nanodegree.

# Deployed Version
The app is deployed and is accessible on heroku: `https://bt-kudos-app.herokuapp.com/`.

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
- `read:kudos` read kudos either individual or multiples
- `create:kudos` create persisten kudo addressed to an existing team member
- `get:team-members` check the list of existing team members


### Manager Role
Managers have the permissions to:
- same as team members
- `patch:kudos` update the contents of a kudo
- `delete:kudos` delete a specific kudo
- `create:team-member` register a team member in the db
- `delete:team-member` delete a team member with all their received kudos

## API Architecture

### KUDO Endpoints
1. `POST /kudos/ create:kudos`
 - Record a new kudo, receives a JSON
 ```
  {
    "text": "Julien, you've done a great job!",
      // must be a valid team member id otherwise is rejected with 400
    "team_member_id": 1, 
    "date": "2020-09-12"
  }
 ```

2. `GET /kudos/ read:kudos`
 - Returns all kudos which are available to the visitor
 ```
  {
    "kudos": [ ... ] // contains all kudos as {id, text}
    "success": 
  }
 ```

3. `GET /kudos/<kudos_id> read:kudos`
 - Returns a specific kudos with id <kudos_id>

4. `PATCH /kudos/<kudos_id> patch:kudos`
 - Updates the content of a specific kudos Returns the updated kudos
 - Receives a JSON with the same format as for POST
 - for non-existing ids returns with 404

5. `DELETE /kudos/<kudos_id> delete:kudo`
 - Deletes a specific kudos Returns the id of the deleted kudos
 - for non-existing ids returns with 404

### Team-member Endpoints
6. `GET /team-members get:team-members`
  - Returns a list of all team members

7. `POST /team-members create:team-members`
  - Manager can add a team member, receives a JSON
```
{
  "name": "Julien",
  "position": "tester"
}
```

8. `DELETE /team-members/<team-member_id> delete:team-members`
 - Delete a specific team member
 - for non-existing ids returns with 404


9. `GET /kudos/team-members/<team-member_id> read:kudos`
 - Returns all kudos given to a specific team member
```
{
  "success":
  "kudos": [{...}, ] // array of kudos
  "team-member": {...} // team-member
}
```

## Database Schema
### Kudos
Representation of the kudo with the fields

```
id - unique id
text - String, literal description of the kudos
date - date of entry in literal format
team_member_id - foreign key, Team-Member id
```

### Team-Member
Representation of the team-member to receive the kudo.

```
id - unique id of the team member
name - name of the team member
position - position of the team member
kudos - all kudos referring to this team member are represented in a one-to-many relationship
```

### Migrations
Database migrations stored at `database/migrations/` contain the script to realize this schema.

## TECH STACK
- API: FLASK, Python
- WSGI: GUNICORN
- ORM: SQL Alchemy
- Dev DB: PostgreSQL (run in Docker)
- Testing: Python Unittest
- Template Render: Jinja2
- Authentication: Auth0

# SETUP & RUNNING

## DEPENDENCIES
Dependencies are stored in `requirements.txt` to be installed with `pip install -r requirements.txt`
For local development a PosgreSQL server was used which ran in a docker container.


## SETUP
### Environment Variables
The API consumes a number of environment variables which are documented in `env/setup_local.sh` and `env/setup_cloud.sh`. These are required to establish the DB connection and the authentication through Auth0. Can be source with `source /env/setup_local.sh`

Locally these can be set by running `env/setup_local.py`.

### Database
Once connected to a running database the migration scripts at `database/migrations/` realize the neccessary schema.

```
cd database/
python manage.py db upgrade
```

## TESTING
Unittest are defined in `tests/test_api.py`. To successfully run all 20 a clean database is needed, some tests refer to hard-wired ids in the database. Current good practice would be mock testing, is foreseen in future versions.

To run the tests a valid `JWT` is needed which can be generated while accessing the app on `https://bt-kudos-app.herokuapp.com/`

```
cd tests/
python -m unittest test_api.py
```