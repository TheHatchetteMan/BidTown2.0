class User:
    #static

    def __init__(self):
        self.identity = {'user_id': None, 'email': None, 'fn': None, 'ln': None, 'location': None, 'type': None}

    def authenticate(self):
