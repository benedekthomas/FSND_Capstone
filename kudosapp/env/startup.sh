docker run -itd -e PGPASS=password1 -e POSTGRES_PASSWORD=password1 -e POSTGRES_USER=benedekthomas -e POSTGRES_DB=trivia -p 5432:5432 --name "PGS_Server" --rm postgres

