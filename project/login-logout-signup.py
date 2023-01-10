import hashlib
from uuid import uuid4


class User:
    """ User class with ID, name and hashed password """
    def __init__(self, username, password):
        self.userID = str(uuid4())
        self.username = username
        self.password = self.hash_password(password)

    def hash_password(self, password):
        """ Hashes the password using SHA-256 """
        return hashlib.sha256(password.encode()).hexdigest()
        ''' explanation:
        password is utf-8 encoded 
        which is needed for sha256 encryption 
        which is then digested into a hexadecimal representation of the bytes object
        '''

    def check_password(self, password):
        """ Returns boolean whether password is correct """
        return self.hash_password(password) == self.password


class AllUsers:
    """ class AllUsers to store every new User instance """
    def __init__(self):
        self.users = {}

    def signup(self, username, password):
        if username in self.users:
            raise ValueError(f"Username {username} is already taken.")
        self.users[username] = User(username, password)

    def login(self, username, password):
        try:
            user = self.users[username]
        except KeyError:
            raise ValueError(f"No such user: {username}")
        if not user.check_password(password):       # returns bool
            raise ValueError("Incorrect password")
        return user
        # TODO: create session token?
        # TODO: grant access to functionality instead of returning user

    def logout(self, user):
        # TODO: invalidate session token?
        pass
