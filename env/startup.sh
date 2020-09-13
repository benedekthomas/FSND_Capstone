docker run -itd -e POSTGRES_PASSWORD=password1 -e POSTGRES_USER=benedekthomas -e POSTGRES_DB=KUDOS_DB -p 5432:5432 --name "PGS_Server" --rm postgres

