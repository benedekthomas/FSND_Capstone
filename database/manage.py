# add parent folder to the python path so relative imports can function
import sys
sys.path.append('..')

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from .kudosapp import app
from .models import db, Team_Member, Kudo, setup_db

setup_db(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    print(__package__)

