from app_config import app
from flask import render_template, request, redirect, session
from DB_Helper import DB_Helper
from BidManager import BidManager
from User import User

#  common objects & data
bm = BidManager()
user = User()

@app.context_processor
def show_logged_in():
    session
    logged_in = None

    if 'bidtown_session_key' in session and len(session['bidtown_session_key']) > 0:
        logged_in = True
    else:
        logged_in = False

    return dict(userLog=logged_in, name=user.get_name(1))


#  ------------------------------------- HOME -------------------------------------  #
@app.route("/")
@app.route('/HomePage')
def view_popular_item():
    item_list = bm.get_top_popular(10)  # paramater specifies how many items to populate. default param is 1
    return render_template("HomePage.html", item_list=item_list)


#  ------------------------------------- TOP SELLERS ---------------------------------------  #
@app.route("/TopSellers")
def view_top_sellers():
    item_list = bm.get_top_sellers(10)
    return render_template("TopSellers.html", item_list=item_list)


#  ------------------------------------- ENDING SOON ---------------------------------------  #
@app.route('/EndingSoon')
def Ending_Soon():
    item_list = bm.get_ending_soon(10)
    return render_template("EndingSoon.html", item_list=item_list)


#  ------------------------------------- CREATE ACCOUNT -------------------------------------  #
@app.route('/CreateAccount', methods=['POST', 'GET'])
def CreateAccount():
    if 'bidtown_session_key' in session and session['bidtown_session_key'] is not None:
        return redirect('/HomePage')  # redirect if logged in
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']
        user_first_name = request.form['FirstName']
        user_last_name = request.form['LastName']
        user_location = request.form['Location']
        user_type = request.form['type']

        db = DB_Helper()
        sql = ('INSERT INTO Users(Email, Password, FirstName, LastName, Location, Type) '
               'VALUES(?, ?, ?, ?, ?, ? )')

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, (user_email, user_password, user_first_name, user_last_name, user_location, user_type, ))
        db.disconnect()

        return redirect('/Login')
    # elif request.method == 'GET'
    return render_template('AccountCreation.html')


#  ------------------------------------- Login -----------------------------------  #
@app.route('/Login')
def Login():
    return render_template('LoginForm.html')


#  ------------------------------------ Test Page----------------------------------  #
@app.route("/item/<int:ItemID>", methods=['GET'])  # testing
def view_single_item(ItemID):
    if request.method == 'GET':
        allow_to_bid = user.bid_allowed()
        return bm.view_item(ItemID, allow_to_bid)
    return "Error fetching single item"


@app.route("/place-bid", methods=['POST'])
def place_bid():
    if request.method == 'POST' and (request.form is not None) or len(request.form) != 0:
        return bm.place_bid()
    return "Error placing a bid"


#------------------------------------ Browse ----------------------------------#
@app.route("/browse")
def search():
    return render_template('Browse.html')


@app.route("/filter", methods=['GET'])
def filter():
    db = DB_Helper()
    Class = request.args['Class']

    item_list = {'item': []}
    attributes = []

    if request.method == "GET" and request.args['Class'] is not None:
        sql = ('SELECT I.ItemID, I.UserID, I.Name, I.Image_Url, I.Status, '
               'I.Current_Bid, I.Bid_Count, I.Start_Date, I.End_Date, C.ClassID, C.ClassType, I.Description '
               f'FROM Item I, Class C, {Class} CT '
               f'WHERE C.ClassType = "{Class}" '
               'AND  I.Status = "For_Sale" AND I.ItemID = CT.ItemID ')

        empty_tuple = ()

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, empty_tuple)

        results = cursor.fetchall()

        for (ItemID, UserID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date, ClassID,
             ClassType, Description) in results:
            item_list['item'].append([ItemID, UserID, Name.decode(), Image_Url.decode(), Status.decode(),
                                      Current_Bid.decode(), Bid_Count, Start_Date, End_Date, ClassID, ClassType.decode(), Description.decode()])

        cursor.close()  # clear cursor but keep db connection

        # new query: get class attributes for the given class ()
        sql = ("SELECT COLUMN_NAME "
               "FROM INFORMATION_SCHEMA.COLUMNS "
               "WHERE TABLE_SCHEMA = 'BidTown' AND TABLE_NAME = ?;")
        cursor = db.connection.cursor(prepared=True)  # new cursor object
        table_name = (Class,)
        cursor.execute(sql, table_name)
        results = cursor.fetchall()

        for (x,) in results:  # including comma tells python to load individual variables not entire tuple to x.
            attributes.append(x.decode())
        cursor.close()

    if len(request.args) > 1:
        checked = []

        for x in range(0, len(attributes)):
            if str(x) in request.args:
                checked.append(request.args[str(x)])

        # attr_name = []
        attr_str = ""
        for each in checked:
            # attr_name.append(each)
            attr_str = attr_str + f"AND CT.{each}=1 "

        no_data = ()

        sql = ("SELECT I.ItemID, I.UserID, I.Name, I.Image_Url, I.Status, "
               "I.Current_Bid, I.Bid_Count, I.Start_Date, I.End_Date, C.ClassID, C.ClassType "
               f"FROM Item I, Class C, {Class} CT "
               f"WHERE C.ClassType = '{Class}' "
               "AND I.Status = 'For_Sale' AND I.ItemID = CT.ItemID AND C.ClassID=CT.ClassID "
               f"{attr_str}")

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, no_data)
        results = cursor.fetchall()

        item_list['item'] = []

        for (ItemID, UserID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date, ClassID, ClassType) in results:
            item_list['item'].append([ItemID, UserID, Name.decode(), Image_Url.decode(), Status, Current_Bid.decode(), Bid_Count, Start_Date, End_Date, ClassID, ClassType.decode()])

    db.disconnect()
    return render_template('Browse.html', item_list=item_list['item'], ClassType=Class, attributes=attributes)


# ------------------------------------ Account ----------------------------------#
@app.route("/Account")
def login():
    return render_template("LoginForm.html")


@app.route('/Login', methods=['POST'])
def signin():
    user_data = user.authenticate()  # authenticate user identity
    user_exists = len(user_data['user']) == 1

    if user_exists:
        info = user.set_session(user_data)  # allow session
        return redirect('/HomePage')
    return render_template("LoginForm.html", Logged_In=user_exists) + "Failed Login"

@app.route('/Logout')
def logout():
    return user.logout()

#  ------------------------------------- CREATE ITEM -------------------------------------  #
@app.route('/ListItem', methods=['POST', 'GET'])
def list_item():
    if 'bidtown_session_key' in session and session['bidtown_session_key'] is not None:

        if request.method == 'POST':
            item_userid= user.get_user_id()
            item_name = request.form['name']
            item_image = request.form['url']
            item_startbid = request.form['start_bid']
            item_startdate = request.form['start_date']
            item_enddate = request.form['end_date']
            item_location = request.form['location']
            item_description = request.form['description']
            item_weight = request.form['weight']
            item_age = request.form['age']
            item_type = request.form['type']

            db = DB_Helper()
            sql = ("INSERT INTO Item(UserID, Name, Image_Url, Status, Start_Bid, Current_Bid, Bid_Count, "
                   "Start_Date, End_Date, "
                   "Location, Description, Weight, Age) "
                   f"VALUES({item_userid}, '{item_name}', '{item_image}', 'For_Sale', {item_startbid}, "
                   f"{item_startbid}, 1, '{item_startdate}', "
                   f"'{item_enddate}', '{item_location}', '{item_description}', "
                   f"{item_weight}, {item_age})")

            empty_tuple = ()

            cursor = db.connection.cursor(prepared=True)
            cursor.execute(sql, empty_tuple)
            cursor.close()
            db.disconnect()

    return render_template("Sell_Item.html")
#  ------------------------------------- CREATE ITEM -------------------------------------  #
@app.route('/AccountDash')
def AccountDash():
    return render_template("AccountDashboard.html")
