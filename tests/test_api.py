import os
import sys
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

# add parent folder to path
sys.path.append('..')

from kudosapp import app
from database.models import setup_db, Kudo, Team_Member

class TeamMemberEndpoints_TestCase(unittest.TestCase):
    """This class represents the test case for kudos api"""
    # (*) GET /team-members/ Returns a list of all team members
    # (*) POST /team-members/ Manager can add a team member.
    # (*) DELETE /team-members/<team-member_id>
    #       Delete a specific team member with all kudos addressed to him/her
    # ( ) GET /kudos/team-members/<team-member_id> Returns
    #       all kudos given to a specific team member
    
    # set manager header JWT
    headers_mg = {
        'Authorization': 'Bearer {}'.format(os.environ['MANAGER_JWT'])
    }

    # set manager header JWT
    headers_tm = {
        'Authorization': 'Bearer {}'.format(os.environ['TEAM_MEMBER_JWT'])
    }

    @classmethod
    def setUpClass(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.DATABASE_URL = os.environ['DATABASE_URL']
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()

        # add 1 team-member
        data = {
            "name": "Julien",
            "position": "tester"
        }
        self.client().post('/team-members', json=data, headers=self.headers_mg)

        # add 1 kudo
        data = {
            "text": "Julien, you've done a great job!",
            "team_member_id": 1,
            "date": "2020-09-12"
        }
        self.client().post('/kudos', json=data, headers=self.headers_mg)

    # #### GET TEAM-MEMBERS ENDPOINT   
    def test_get_team_members_noauth(self):
        """ Test accessing endpoint w/o authorization """
        response = self.client().get('/team-members')
        self.assertEqual(response.status_code, 401)

    def test_get_team_members_auth(self):
        """ Test accessing endpoint w authorization requiring get:team-members"""
        response = self.client().get('/team-members', headers=self.headers_mg)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(json.loads(response.data)['team-members']), 1)
    
    # #### POST TEAM-MEMBERS ENDPOINT   
    def test_post_team_member_noauth(self):
        """ Test accessing endpoint w/o authorization """
        response = self.client().post('/team-members')
        self.assertEqual(response.status_code, 401)

    def test_post_team_member_auth_mg(self):
        """ Test accessing endpoint w manager authorization requiring create:team-member"""
        data = {
            "name": "Julien",
            "position": "tester"
        }
        response = self.client().post('/team-members', json=data, headers=self.headers_mg)
        self.assertEqual(response.status_code, 201)

    def test_post_team_member_auth_tm(self):
        """ Test accessing endpoint w team-member authorization requiring create:team-member"""
        data = {
            "name": "Julien",
            "position": "tester"
        }
        response = self.client().post('/team-members', json=data, headers=self.headers_tm)
        self.assertEqual(response.status_code, 403)

    def test_post_team_member_auth_bad_req(self):
        """ Test accessing endpoint w manager authorization 
        requiring create:team-member, bad request"""
        data = {
            "name": None,
            "position": "tester"
        }
        response = self.client().post('/team-members', json=data, headers=self.headers_mg)
        self.assertEqual(response.status_code, 400)

    # #### DELETE TEAM-MEMBERS ENDPOINT
    def test_delete_team_member_noauth(self):
        """ Test accessing endpoint w/o authorization """
        response = self.client().delete('/team-members/2')
        self.assertEqual(response.status_code, 401)

    def test_delete_team_member_auth(self):
        """ Test accessing endpoint w authorization """
        response = self.client().delete('/team-members/2', headers=self.headers_mg)
        self.assertEqual(response.status_code, 200)

    def test_delete_team_member_auth_404(self):
        """ Test accessing endpoint w authorization missing resource"""
        response = self.client().delete('/team-members/999', headers=self.headers_mg)
        self.assertEqual(response.status_code, 404)

    # #### GET KUDOS FOR A TEAM-MEMBER ENDPOINT
    def test_get_kudos_for_a_team_member_noauth(self):
        """ Test accessing endpoint w/o authorization """
        response = self.client().get('kudos/team-members/1')
        self.assertEqual(response.status_code, 401)

    def test_get_kudos_for_a_team_member_auth(self):
        """ Test accessing endpoint w/o authorization """
        response = self.client().get('kudos/team-members/1', headers=self.headers_mg)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(data['kudos']), 1)

class KudoEndpoints_TestCase(unittest.TestCase):
    """This class represents the test case for kudos api"""
    # set manager header JWT
    headers_mg = {
        'Authorization': 'Bearer {}'.format(os.environ['MANAGER_JWT'])
    }

    # set manager header JWT
    headers_tm = {
        'Authorization': 'Bearer {}'.format(os.environ['TEAM_MEMBER_JWT'])
    }

    @classmethod
    def setUpClass(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.DATABASE_URL = os.environ['DATABASE_URL']
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()

        # add 1 team-member
        data = {
            "name": "Julien",
            "position": "tester"
        }
        self.client().post('/team-members', json=data, headers=self.headers_mg)

        # add 1 kudo
        data = {
            "text": "Julien, you've done a great job!",
            "team_member_id": 1,
            "date": "2020-09-12"
        }
        self.client().post('/kudos', json=data, headers=self.headers_mg)

    # #### GET KUDOS ENDPOINT
    def test_get_kudos_noauth(self):
        """ Test accessing endpoint w/o authorization """
        response = self.client().get('/kudos')
        
        self.assertEqual(response.status_code, 401)

    def test_get_kudos_auth(self):
        """ Test accessing endpoint w authorization requiring read:kudos"""
        response = self.client().get('/kudos', headers=self.headers_mg)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(data['kudos']), 1)

    # #### GET ONE KUDO ENDPOINT
    def test_get_one_kudo_noauth(self):
        """ Test accessing endpoint w/o authorization """
        response = self.client().get('/kudos/1')
        
        self.assertEqual(response.status_code, 401)

    def test_get_one_kudo_auth(self):
        """ Test accessing endpoint w authorization requiring read:kudos"""
        response = self.client().get('/kudos/1', headers=self.headers_mg)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['kudo']['id'], 1)

    # #### POST KUDO ENDPOINT
    def test_post_a_kudo_noauth(self):
        """ Test accessing endpoint w/o authorization """
        kudo = {
            "text": "Julien, you've done a great job!",
            "team_member_id": 1,
            "date": "2020-09-12"
        }
        response = self.client().post('/kudos', json=kudo)
        self.assertEqual(response.status_code, 401)

    def test_post_a_kudo_bad_request(self):
        """ Test accessing endpoint w authorization bad request"""
        kudo = {
            "text": None,
            "team_member_id": 9999,
            "date": "2020-09-12"
        }
        response = self.client().post('/kudos', json=kudo, headers=self.headers_mg)
        self.assertEqual(response.status_code, 400)

    def test_post_a_kudo_auth(self):
        """ Test accessing endpoint w authorization requiring create:kudo"""
        kudo = {
            "text": "Julien, you've done a great job!",
            "team_member_id": 1,
            "date": "2020-09-12"
        }
        response = self.client().post('/kudos', json=kudo, headers=self.headers_mg)
        self.assertEqual(response.status_code, 201)

    # #### PATCH A KUDO ENDPOINT
    def test_patch_a_kudo_noauth(self):
        """ Test accessing endpoint w authorization """
        response = self.client().patch('/kudos/1')
        self.assertEqual(response.status_code, 401)

    def test_patch_a_kudo_auth(self):
        """ Test accessing endpoint w authorization """
        kudo = {
            "text": "You are updated",
            "team_member_id": 1,
            "date": "1111-11-11"
        }
        response = self.client().patch('/kudos/1', json=kudo, headers=self.headers_mg)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

    
    @classmethod
    def tearDownClass(self):
        """Executed after reach test"""
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()