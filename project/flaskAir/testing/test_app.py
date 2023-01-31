import unittest
from website import create_app, create_admin, db, ADMIN_MAIL
from website.models import User



class TestAppSetup(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        

    def test_create_admin(self):
        """
        test whether the app has a connection to the user database
        """
        with self.app.app_context():
            create_admin()
            admin = db.session.execute(db.select(User).filter_by(email=ADMIN_MAIL)).scalar_one()
            print(admin)
            self.assertIsNotNone(admin)
            self.assertTrue(admin.is_admin)
    
    def tearDown(self):
        del self.app

if __name__ == "__main__":
    unittest.main()