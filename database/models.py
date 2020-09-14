import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()
DATABASE_URL = os.environ['DATABASE_URL']
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
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
Team_Member
    a persistent Team_Member entry, extends the base SQLAlchemy Model
'''
class Team_Member(db.Model):
    __tablename__ = "team_members"

    # Autoincrementing, unique primary key
    id = Column(Integer(), primary_key=True)
    # String, name of the team member
    name = Column(String(120), nullable=False)
    # String, work position of the team member
    position = Column(String(80))
    # Definition of the kudoses relationship btw team member (who got the kudos) and the kudos
    kudos = db.relationship("Kudo", backref="kudos", cascade="all,delete")

    '''
    display()
        returns the complete representation of the model entry
    '''
    def display(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position
        }

    '''
    insert()
        inserts a new model into a database
        the model must contain a name
        EXAMPLE
            team_member = Team_Member(name=req_name, position=position)
            team_member.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes an existing model from the database
        the model must exist in the database
        EXAMPLE
            team_member = Team_Member(name=req_name, position=position)
            team_member.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates an existing model in the database
        EXAMPLE
            team_member = Team_Member.query.filter(Team_Member.id == id).one_or_none()
            team_member.position = 'CEO'
            team_member.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.display())


'''
Kudo
    a persistent Kudo entry, extends the base SQLAlchemy Model
'''
class Kudo(db.Model):
    __tablename__ = "kudos"

    # Autoincrementing, unique primary key
    id = Column(Integer(), primary_key=True)
    # String Kudo
    text = Column(String(200))
    # Integer, foreign key reference to team member
    team_member_id = Column(Integer, db.ForeignKey("team_members.id"), nullable=False)
    # Date, stores the entry date in YYYY-MM-DD form
    date =  Column(String(10), nullable=True)

    '''
    short()
        short form representation of the Kudos model
    '''
    def short(self):
        return {
            'id': self.id,
            'text': self.text,
        }

    '''
    long()
        long form representation of the Kudos model
    '''
    def long(self):
        return {
            'id': self.id,
            'text': self.text,
            'team_member': self.team_member_id,
            'date': self.date
        }

    '''
    insert()
        inserts a new model into a database
        the model must contain a kudos text
        the model must contain a valid team_member_id
        EXAMPLE
            kudo = Kudo(text=req_text, team_member_id=req_team_member_id)
            kudo.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        deletes an existing model from the database
        EXAMPLE
            kudo = Kudo(text=req_text, team_member_id=req_team_member_id)
            kudo.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            kudo = Kudo.query.filter(Kudo.id == id).one_or_none()
            kudo.text = 'You are great!'
            kudo.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())

