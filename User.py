from flask import request, redirect, render_template, session, make_response
from DB_Helper import DB_Helper

class User:
    #static

    def __init__(self):
        self.identity = {'user_id': None, 'email': None, 'fn': None, 'ln': None, 'location': None, 'type': None}

    def authenticate(self):
        if request.method == 'POST':
            email_entered = request.form['email']  # get form data from user
            password_entered = request.form['password']
            user_data = {'user': []}
            user_exists = False

            db = DB_Helper()  # open db resources
            sql = (f"SELECT UserID, Email, Password, FirstName, LastName, Location, Type "
                   "FROM Users "
                   f"WHERE Users.email = '{email_entered}' AND Users.password = '{password_entered}'")

            empty_tuple = ()

            cursor = db.connection.cursor(prepared=True)
            cursor.execute(sql, empty_tuple)
            results = cursor.fetchall()

            for (UserID, email, password, FirstName, LastName, Location, Type) in results:  # get data
                user_data['user'].append([UserID, email.decode(), password.decode(), FirstName.decode(),
                                          LastName.decode(), Location.decode(), Type])
            db.disconnect()  # close db resources

            user_exists = len(user_data['user']) == 1

            if user_exists:  # set user data object
                self.identity['user_id'] = user_data['user'][0][0]  # list[row][data index]
                self.identity['email'] = user_data['user'][0][1]
                self.identity['fn'] = user_data['user'][0][3]
                self.identity['ln'] = user_data['user'][0][4]
                self.identity['location'] = user_data['user'][0][5]
                self.identity['type'] = user_data['user'][0][6]

            return user_data

    def set_session(self, user_data):
        session['bidtown_session_key'] = user_data['user']  # grant user access with session cookie
        return session['bidtown_session_key']

    def is_buyer(self):
        return self.identity['type'] == 0

    def is_seller(self):
        return self.identity['type'] == 1

    def is_admin(self):
        return self.identity['type'] == 2

    def get_name(self, name=3):
        """Get the name of the user. 3 options: 1=firstname only, 2=lastname only, 3=fullname... else None"""
        if name == 3:
            return self.identity['fn'] + " " + self.identity['ln']
        elif name == 2:
            return self.identity['ln']
        elif name == 1:
            return self.identity['fn']
        return None

    def get_email(self):
        return self.identity['email']

    def get_location(self):
        return self.identity['location']

    def get_user_id(self):
        return self.identity['user_id']

    def is_logged_in(self):
        """General login check. Check that a session cookie exists regardless of account type"""
        return 'bidtown_session_key' in session and self.session_size('bidtown_session_key') == 6

    def session_size(self, session_key_name):
        """Gets session data list size. Returns -1 to indicate session doesn't exist"""
        if session_key_name in session:
            return len(session[session_key_name])
        return -1

    def bid_allowed(self):
        return self.is_buyer()

    def clear_identity(self):
        self.identity = {'user_id': None, 'email': None, 'fn': None, 'ln': None, 'location': None, 'type': None}
        return self.identity()

    def logout(self):
        if self.is_logged_in():
            self.clear_identity()
        session.pop('bidtown_session_key', None)
        res = make_response(render_template('LoginForm.html'))
        res.set_cookie('session', max_age=0)
        return res
