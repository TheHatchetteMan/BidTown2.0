from app_config import app
from flask import render_template, request, redirect, url_for, flash
from DB_Helper import DB_Helper

# @app.context_processor  # use this for loading base.html layout with common elements among views

@app.route("/")
def base():
    return render_template("base.html")
	
#------------------------------------- HOME -------------------------------------#
@app.route('/')
@app.route('/HomePage')
def HomePage():
    return render_template('HomePage.html')

#------------------------------------- CREATE ACCOUNT -------------------------------------#
@app.route('/')
@app.route('/HomePage')
@app.route('/CreateAccount')
def CreateAccount():
	return render_template('AccountCreation.html')

#------------------------------------- Login -----------------------------------#
@app.route('/')
@app.route('/HomePage')
@app.route('/Login')
def Login():
	return render_template('LoginForm.html')

#------------------------------------ Test Page----------------------------------#
@app.route("/single-item")  # testing
def view_single_item():
    db = DB_Helper()
    sql = ("SELECT ItemID, UserID, ClassID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date " \
          "FROM Item")
    no_data = ()  # for prepared statement functionality
    cursor = db.connection.cursor(prepared=True)
    cursor.execute(sql, no_data)

    results = cursor.fetchall()

    item_data = {}

    for (ItemID, UserID, ClassID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date) in results:
        item_data['item'] = [ItemID, UserID, ClassID, Name.decode(), Image_Url.decode(), Status, Current_Bid.decode(), Bid_Count, Start_Date, End_Date]

    db.disconnect(commit=True)
    return render_template("ItemForm.html", item_data=item_data)

@app.route("/place-bid", methods=['POST'])
def place_bid():
    if request.method == 'POST' and (request.form is not None) or len(request.form) != 0:
        db = DB_Helper()

        # data
        bid_increment = float(request.form['bid'])
        Item_ID = request.form['item-id']
        expected_bidcount = int(request.form['expected-bidcount'])
        expected_bid_total = float(request.form['expected-bid']) + bid_increment

        # check that bid expectation is what will actually happen AKA recheck for actual bid and bid count match
        cursor = db.connection.cursor()
        cursor.execute(f"SELECT Current_Bid, Bid_Count FROM Item WHERE ItemID={Item_ID}")
        actual_bidcount = -1
        actual_current_bid = bid_increment
        for (Current_Bid, Bid_Count) in cursor:
            actual_bidcount = Bid_Count
            actual_current_bid = float(Current_Bid)
        cursor.close()

        actual_bid_total = actual_current_bid + bid_increment

        meets_count = expected_bidcount == actual_bidcount  # is the user behind in their attempt to bid
        meets_expected_bid = expected_bid_total == actual_bid_total  # does the user's expected bid match what will be updated

        if meets_count and meets_expected_bid:
            sql = ("UPDATE Item "
                   "SET Current_Bid = Current_Bid + ?, Bid_Count = Bid_Count + 1 "
                   f"WHERE ItemID = ? AND Bid_Count = {actual_bidcount} "
                   "AND Current_Bid < (Current_Bid + ?) "  # adding negative & zero amounts
                   )  # check bid count at database level
            # cursor.close()
            update = db.connection.cursor(prepared=True)
            update.execute(sql, (bid_increment, Item_ID, expected_bidcount,))
            db.disconnect()
            return "Success"
        else:
            db.disconnect()
            return "You snooze, you lose! Someone else placed a bid while you were looking at the item"
