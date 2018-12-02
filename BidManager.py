from flask import request, render_template, redirect
from DB_Helper import DB_Helper

class BidManager:
    # static/shared data

    def __init__(self):
        self.item = {'expected-bidcount': None, 'expected-bid': None}

    def clear_item(self):
        self.item['expected-bid'] = None
        self.item['expected-bidcount'] = None

    def place_bid(self):  # must be called after view_item(id)
        db = DB_Helper()

        # data
        bid_increment = float(request.form['bid'])
        item_id = request.form['item-id']
        expected_bidcount = self.item['expected-bidcount']
        expected_bid_total = float(self.item['expected-bid']) + bid_increment

        # check that bid expectation is what will actually happen AKA recheck for actual bid and bid count match
        cursor = db.connection.cursor()
        cursor.execute(f"SELECT Current_Bid, Bid_Count FROM Item WHERE ItemID={item_id}")
        actual_bidcount = -1
        actual_current_bid = bid_increment
        for (Current_Bid, Bid_Count) in cursor:
            actual_bidcount = Bid_Count
            actual_current_bid = float(Current_Bid)
        cursor.close()
        actual_bid_total = actual_current_bid + bid_increment

        # is the user behind in their attempt to bid
        # if the user updates their bid, will the resulting bid amount be what they were expecting
        meets_expectation = (expected_bidcount == actual_bidcount) and (expected_bid_total == actual_bid_total)

        if meets_expectation:
            sql = ("UPDATE Item "
                   "SET Current_Bid = Current_Bid + ?, Bid_Count = Bid_Count + 1 "
                   f"WHERE ItemID = ? AND Bid_Count = {actual_bidcount} "
                   "AND Current_Bid < (Current_Bid + ?) "  # adding negative & zero amounts
                   )  # check bid count at database level
            update = db.connection.cursor(prepared=True)
            update.execute(sql, (bid_increment, item_id, expected_bidcount,))
            db.disconnect()

            self.clear_item()
            return redirect("/single-item/{id}".format(id=item_id))

        self.clear_item()
        db.disconnect()
        return redirect("/single-item/{id}".format(id=item_id))
                                                                                                               
    def view_item(self, id):  # must be called before place_bid()
        db = DB_Helper()
        sql = ("SELECT ItemID, UserID, ClassID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date "
               "FROM Item "
               "WHERE ItemID=?")
        data = (id,)  # for prepared statement functionality. not sure if this is required.
        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, data)

        results = cursor.fetchall()

        item_data = {}

        for (ItemID, UserID, ClassID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date) in results:
            item_data['item'] = [ItemID, UserID, ClassID,
                                 Name.decode(),
                                 Image_Url.decode(),
                                 Status,
                                 Current_Bid.decode(),
                                 Bid_Count,
                                 Start_Date,
                                 End_Date]

        self.item['expected-bidcount'] = item_data['item'][7]
        self.item['expected-bid'] = item_data['item'][6]

        db.disconnect(commit=True)
        return render_template("ItemForm.html", item_data=item_data)

    def get_top_popular(self, limit=1):
        db = DB_Helper()
        sql = ('SELECT ItemID, UserID, ClassID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date '
               'FROM Item ORDER BY Bid_Count DESC LIMIT ?')

        data = (limit,)  # to satisfy execute method for prepared statement

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, data)
        results = cursor.fetchall()

        item_list = {'item': []}

        for (ItemID, UserID, ClassID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date) in results:
            item_list['item'].append(
                [ItemID, UserID, ClassID, Name.decode(), Image_Url.decode(), Status, Current_Bid.decode(), Bid_Count,
                 Start_Date, End_Date])

        db.disconnect()
        return item_list
