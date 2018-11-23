from app_config import app
from flask import render_template, request
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
        item_data['item'] = [ItemID, UserID, ClassID, Name.decode(), Image_Url, Status, Current_Bid.decode(), Bid_Count, Start_Date, End_Date]

    db.disconnect(commit=True)
    return render_template("/ItemForm.html", item_data=item_data)

@app.route("/place-bid", methods=['POST'])
def place_bid():
    # if request.method == 'POST':
    #     request.form[]
    pass