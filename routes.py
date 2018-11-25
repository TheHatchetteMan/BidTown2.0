from app_config import app
from flask import render_template, request, redirect
from DB_Helper import DB_Helper

# @app.context_processor  # use this for loading base.html layout with common elements among views

@app.route("/")
def base():
	return render_template("base.html")

#------------------------------------- HOME -------------------------------------#
@app.route('/HomePage')
def view_popular_item():
    db = DB_Helper()
    sql = ('SELECT ItemID, UserID, ClassID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date '
           'FROM Item ORDER BY Bid_Count DESC LIMIT 10')

    empty_tuple = ()

    cursor = db.connection.cursor(prepared=True)
    cursor.execute(sql, empty_tuple)

    results = cursor.fetchall()

    item_list = {}
    item_list['item'] = []

    for (ItemID, UserID, ClassID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date) in results:
        item_list['item'].append([ItemID, UserID, ClassID, Name.decode(), Image_Url.decode(), Status, Current_Bid.decode(), Bid_Count, Start_Date, End_Date])

    db.disconnect()
    return render_template("HomePage.html", item_list=item_list)

#------------------------------------- CREATE ACCOUNT -------------------------------------#
@app.route('/CreateAccount')
def CreateAccount():
	return render_template('AccountCreation.html')

#------------------------------------- Login -----------------------------------#
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
	if request.method == 'POST' and (request.form != None) or len(request.form) != 0:
		bid = request.form['bid']
		Item_ID = request.form['item-id']
		expected_bidcount = request.form['expected-bidcount']

		db = DB_Helper()
		sql = ("UPDATE Item "
			   "SET Current_Bid = Current_Bid + ?, Bid_Count = Bid_Count + 1 "
			   f"WHERE ItemID = ? AND Bid_Count = {expected_bidcount}"
			   )

		update = db.connection.cursor(prepared=True)
		update.execute(sql, (bid, Item_ID,))
		db.disconnect()
		return redirect("/single-item")
	return "Error"
#------------------------------------ Browse ----------------------------------#
@app.route("/browse")
def search():
    return render_template('Browse.html')

@app.route("/filter", methods=['POST'])
def filter():
    if request.method == "POST":
        Class = request.form['Class']
        db = DB_Helper()
        sql = ('SELECT I.ItemID, I.UserID, I.ClassID, I.Name, I.Image_Url, I.Status, '
               'I.Current_Bid, I.Bid_Count, I.Start_Date, I.End_Date, C.ClassID, C.ClassType '
               'FROM Item I, Class C '
               f'WHERE C.ClassType = "{Class}" '
               'AND  I.ClassID = C.ClassID ')

        empty_tuple = ()

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, empty_tuple)

        results = cursor.fetchall()

        item_list = {}
        item_list['item'] = []

        for (ItemID, UserID, ClassID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date, ClassID, ClassType) in results:
            item_list['item'].append([ItemID, UserID, ClassID, Name.decode(), Image_Url.decode(), Status, Current_Bid.decode(), Bid_Count, Start_Date, End_Date, ClassID, ClassType.decode()])

        db.disconnect()

        return render_template('Browse.html', item_list=item_list['item'], ClassType=Class)
