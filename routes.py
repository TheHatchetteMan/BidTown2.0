from app_config import app
from flask import render_template, request, redirect, session
from DB_Helper import DB_Helper
from BidManager import BidManager

#  common objects & data
bm = BidManager()


@app.context_processor
def show_logged_in():
    session
    logged_in = None

    if 'bidtown_session_key' in session and len(session['bidtown_session_key']) > 0:
        logged_in = True
    else:
        logged_in = False

    return dict(userLog=logged_in)


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
    return render_template('AccountCreation.html')


#  ------------------------------------- Login -----------------------------------  #
@app.route('/Login')
def Login():
    return render_template('LoginForm.html')


#  ------------------------------------ Test Page----------------------------------  #
@app.route("/item/<int:ItemID>", methods=['GET'])  # testing
def view_single_item(ItemID):
    if request.method == 'GET':
        return bm.view_item(ItemID)
    return "Error fetching single item"


@app.route("/place-bid", methods=['POST'])
def place_bid():
    if request.method == 'POST' and (request.form is not None) or len(request.form) != 0:
        return bm.place_bid()
    return "Error placing a bid"

    #     db = DB_Helper()
    #     sql = ("UPDATE Item "
    #            "SET Current_Bid = Current_Bid + ?, Bid_Count = Bid_Count + 1 "
    #            f"WHERE ItemID = ? AND Bid_Count = {expected_bidcount}"
    #            )
    #
    #     update = db.connection.cursor(prepared=True)
    #     update.execute(sql, (bid, Item_ID,))
    #     db.disconnect()
    #     return redirect(f"/item/{Item_ID}")
    # return "Error"


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
        sql = ('SELECT I.ItemID, I.UserID, I.ClassID, I.Name, I.Image_Url, I.Status, '
               'I.Current_Bid, I.Bid_Count, I.Start_Date, I.End_Date, C.ClassID, C.ClassType '
               'FROM Item I, Class C '
               f'WHERE C.ClassType = "{Class}" '
               'AND  I.Status = "For_Sale" AND I.ClassID = C.ClassID ')

        empty_tuple = ()

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, empty_tuple)

        results = cursor.fetchall()

        for (ItemID, UserID, ClassID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date, ClassID, ClassType) in results:
            item_list['item'].append([ItemID, UserID, ClassID, Name.decode(), Image_Url.decode(), Status.decode(), Current_Bid.decode(), Bid_Count, Start_Date, End_Date, ClassID, ClassType.decode()])

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

        sql = ("SELECT I.ItemID, I.UserID, I.ClassID, I.Name, I.Image_Url, I.Status, "
               "I.Current_Bid, I.Bid_Count, I.Start_Date, I.End_Date, C.ClassID, C.ClassType "
               f"FROM Item I, Class C, {Class} CT "
               f"WHERE C.ClassType = '{Class}' "
               "AND I.Status = 'For_Sale' AND I.ClassID = C.ClassID AND C.ClassID=CT.ClassID "
               f"{attr_str}")

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, no_data)
        results = cursor.fetchall()

        item_list['item'] = []

        for (ItemID, UserID, ClassID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date, ClassID, ClassType) in results:
            item_list['item'].append([ItemID, UserID, ClassID, Name.decode(), Image_Url.decode(), Status, Current_Bid.decode(), Bid_Count, Start_Date, End_Date, ClassID, ClassType.decode()])

    db.disconnect()
    return render_template('Browse.html', item_list=item_list['item'], ClassType=Class, attributes=attributes)


# ------------------------------------ Account ----------------------------------#
@app.route("/Account")
def login():
    return render_template("LoginForm.html")


@app.route('/Login', methods=['POST', 'GET'])
def authenticate():
    user_exists = False
    if request.method == 'POST':
        userEmail = request.form['email']
        userPassword = request.form['password']
        user_exist_list = {'user': []}

        db = DB_Helper()
        sql = (f'SELECT UserID, "{userEmail}", "{userPassword}", FirstName, LastName, Location, Type '
               'FROM Users '
               f'WHERE Users.email = "{userEmail}" AND Users.password = "{userPassword}"')

        empty_tuple = ()

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, empty_tuple)
        results = cursor.fetchall()

        user_exist_list['user'] = []

        userInt = 0
        for (UserID , email, password, FirstName, LastName, Location, Type ) in results:
            user_exist_list['user'].append(
                [UserID, email.decode(), password.decode(), FirstName.decode(), LastName.decode(),
                 Location.decode(), Type])

        db.disconnect()

        userInt = len(user_exist_list['user'])

        if userInt == 1:
            user_exists = True
            session['bidtown_session_key'] = user_exist_list['user']
            return redirect('/HomePage')
            # return str(user_exists)
        else:
            return render_template("LoginForm.html", Logged_In = user_exists)
            # return str(user_exists)

    return render_template('LoginForm.html', user_exists = user_exists)
