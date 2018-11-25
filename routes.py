from app_config import app
from flask import render_template, request, redirect, url_for, flash
from DB_Helper import DB_Helper
from BidManager import BidManager

# static
bm = BidManager()

# @app.context_processor  # use this for loading base.html layout with common elements among views

@app.route("/")
def base():
	return render_template("base.html")

#  ------------------------------------- HOME -------------------------------------  #
@app.route('/HomePage')
def view_popular_item():
    db = DB_Helper()
    sql = ('SELECT ItemID, UserID, ClassID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date '
           'FROM Item ORDER BY Bid_Count DESC LIMIT 10')

    empty_tuple = ()  # to satisfy execute method for prepared statement

    cursor = db.connection.cursor(prepared=True)
    cursor.execute(sql, empty_tuple)

    results = cursor.fetchall()

    item_list = {}
    item_list['item'] = []

    for (ItemID, UserID, ClassID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date) in results:
        item_list['item'].append([ItemID, UserID, ClassID, Name.decode(), Image_Url.decode(), Status, Current_Bid.decode(), Bid_Count, Start_Date, End_Date])

    db.disconnect()
    return render_template("HomePage.html", item_list=item_list)

#  ------------------------------------- CREATE ACCOUNT -------------------------------------  #
@app.route('/CreateAccount')
def CreateAccount():
	return render_template('AccountCreation.html')

#  ------------------------------------- Login -----------------------------------  #
@app.route('/Login')
def Login():
	return render_template('LoginForm.html')

#  ------------------------------------ Test Page----------------------------------  #

@app.route("/single-item/<int:ItemID>", methods=['GET'])  # testing
def view_single_item(ItemID):
	if request.method == 'GET':
		return bm.view_item(ItemID)
	return "Error fetching single item"

@app.route("/place-bid", methods=['POST'])  # executed on ItemForm.html view
def place_bid():
	if request.method == 'POST' and (request.form is not None) or len(request.form) != 0:
		return bm.place_bid()
	return "Error placing a bid"
