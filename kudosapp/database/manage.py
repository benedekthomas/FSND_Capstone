from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.api import app
from models import db, Team_Member, Kudos, setup_db

setup_db(api)

migrate = Migrate(api, db)
manager = Manager(api)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    print(__package__)

