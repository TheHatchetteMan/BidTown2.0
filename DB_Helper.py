import mysql.connector
from mysql.connector import errorcode

#  provide the correct file path to the database connection configuration file
#filepath = r'C:\\Users\\etwit\\Documents\\USC FALL 18\\CSCI 521\\repository\\mysqlconnection.txt'
#filepath = '/home/edwin/Documents/projects/ab_db_cnxn.txt' # chris uncomment this
filepath = r'C:\\Users\\Terrell\\Documents\\GitHub\\autobuddy_official\\mysqlconnection.txt' # Terrell uncomment this
#filepath = r'C:\\Users\\bryan\\OneDrive\\Documents\\GitHub\\autobuddy_official\\mysqlconnection.txt'
#filepath = r'C:\\Users\\etwit\\Documents\\USC FALL 18\\CSCI 521\\repository\\mysqlconnection.txt' #erin uncomment this

def read_mysql_config(filepath):
    '''
    INPUT: file path pointing to mysql connection information, type: string
    OUTPUT: dictionary contianing key/value pairs of connection info keys:
                'user', 'password','host', 'database'
    '''

    try:
        mysql_config = open(filepath, mode='r')
        contents = mysql_config.read().split()

        connection_info = {}

        connection_info['user'] = contents[0]
        connection_info['password'] = contents[1]
        connection_info['host'] = contents[2]
        connection_info['database'] = contents[3]

        mysql_config.close()

    except FileNotFoundError as FNFE:
        print(f"The file was not found: {FNFE}")

    #print(connection_info)

    return connection_info


class DB_Helper():

    #static variables go here. no need to declare static. Anything here is always static AKA shared with all objects.
    #connection_info = read_mysql_config(filepath)
    #print(connection_info)


    def __init__(self, prep_stmt=False): #attrib=None means default value is none if arg is not passed in
        '''
        INPUT: No parameters. However, reads from mysqlconnection file.
        Builds a connection dictionary. When this object's connect() method is called
        the connection dictionary is passed into mysql.connector.connect( HERE ) as an argument.
        OUTPUT: A database connection is returned to self.connection & a cursor object may be called from it.

        note: the disconnect method must be called to end a db connection, obj.disconnect()

        Intent: to hide the details of and reuse standard connection procedures for making database queries to mysql
        '''
        self.connection_dictionary = read_mysql_config(filepath)
        self.connection_string = None  # used for displaying current connection information
        self.connection = self.connect()
        # self.query_cursor = self.connection.cursor(prepared=prep_stmt)


    #show current connection configuration
    def display_connection_info(self):
        '''Show current connection configuration'''
        self.connection_string = "\n - db connection info - \n" \
                                  f"\nUSER: {self.connection_dictionary['user']}\n" \
                                  f"PASS: {self.connection_dictionary['password']}\n" \
                                  f"HOST: {self.connection_dictionary['host']}\n" \
                                  f"DBNM: {self.connection_dictionary['database']}\n"
        print(self.connection_string)

    #connect/disconnect
    def connect(self):
        '''Attempts to make a connection to the DBMS server.
            If successful, a db connection is returned
            else error message produced.'''
        try:
            return mysql.connector.connect(**self.connection_dictionary)
        except mysql.connector.Error as MySQLError:
            if MySQLError.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Your username or password is incorrect.")
            elif MySQLError.errno == errorcode.ER_BAD_DB_ERROR:
                print("That database name does not exist.")
            else:
                print(f"{MySQLError}")
                print("Connection information:\n")
                self.display_connection_info()

    def commit(self):
        self.connection.commit()

    def disconnect(self, commit=True):
        if commit:
            self.connection.commit()
        self.connection.close()
