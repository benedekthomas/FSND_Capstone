import os

os.system('source setup_local.sh')

# Startup postgres server in docker container
os.system('docker stop PGS_Server')
os.system('docker run -itd -e POSTGRES_PASSWORD=password1 -e POSTGRES_USER=benedekthomas -e POSTGRES_DB=KUDOS_DB -p 5432:5432 \
    --name "PGS_Server" --rm postgres')

# Execute DB upgrade
print("run \n \n python manage.py db upgrade \n \n in database package")