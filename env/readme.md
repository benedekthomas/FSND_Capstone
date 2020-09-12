Helper scripts and files to setup the environment for running locally.

## DATABASE CONNECTION

### PyEnv Virtual Environment
PyEnv was used for development purposes and the virtual environment files are stored locally.

### STARTUP A POSTGRES SERVER DOCKER CONTAINER - `<startup.sh>`
Contains a the startup commands for a postgres docker container in the following format.
```
docker run -itd -e POSTGRES_PASSWORD=<your password> -e POSTGRES_USER=<your user> -e POSTGRES_DB=<DB_NAME> -p 5432:5432 --name "PGS_Server" --rm postgres
```

### STOP THE POSTGRES SERVER - `<stop.sh>`
Contains a the stop commands for the postgres container
```
docker stop PGS_Server
```

### SETUP THE DATABASE - `<set_db.sh>`
```
CREATEDB -h 127.0.0.1 -U <your_user> <DB_NAME>
```