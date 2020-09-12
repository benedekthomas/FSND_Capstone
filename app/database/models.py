import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_psw = os.getenv('DB_PSW')
db_host = 'localhost:5432'
database_URI = "posgresql://{}:{}@{}/{}".format(db_user, db_psw, db_host, db_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Kudos
    a persistent Kudos entry, extends the base SQLAlchemy Model
'''
class Drink(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer(), primary_key=True)
    # String Kudos
    kudos_text = Column(String(80))
    # Integer, foreign key reference to team member
    team_member_id = Column(Integer, db.ForeignKey("TeamMember.id"), nullable=False)
    # Date, stores the entry date in literal form
    date =  Column(String(180), nullable=True)

    '''
    short()
        short form representation of the Kudos model
    '''
    def short(self):
        return {
            'id': self.id,
            'kudos': self.kudos_text,
        }

    '''
    long()
        long form representation of the Kudos model
    '''
    def long(self):
        return {
            'id': self.id,
            'kudos': self.kudos_text,
            'team_member': self.team_member,
            'date': self.date
        }

    '''
    insert()
        inserts a new model into a database
        the model must contain a kudos text
        the model must contain a valid team_member_id
        EXAMPLE
            kudos = Kudos(kudos_text=req_kudos_text, team_member_id=req_team_member_id)
            kudos.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            kudos = Kudos(kudos_text=req_kudos_text, team_member_id=req_team_member_id)
            kudos.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            kudos = Kudos.query.filter(Kudos.id == id).one_or_none()
            kudos.kudos_text = 'You are great!'
            kudos.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())