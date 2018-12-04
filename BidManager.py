from flask import request, render_template, redirect, session
from DB_Helper import DB_Helper

class BidManager:
    # static/shared data

    def __init__(self):
        self.item = {'expected-bidcount': None, 'expected-bid': None}

    def clear_item(self):
        self.item['expected-bid'] = None
        self.item['expected-bidcount'] = None

    def place_bid(self):  # must be called after view_item(id)
        # data
        bid_increment = float(request.form['bid'])
        item_id = int(request.form['item-id'])  # needs to be int for query
        expected_bidcount = self.item['expected-bidcount']
        expected_bid_total = self.item['expected-bid'] + bid_increment
        userid = None

        is_buyer = self.get_user_type() is "buyer"

        db = DB_Helper()
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
        meets_expectation = (expected_bidcount == actual_bidcount) \
                            and (expected_bid_total == actual_bid_total) and \
                            is_buyer
        userid = self.get_user_id()  # if userid == -1 at run time, get_user_id failed to get session info
        if meets_expectation:
            sql = ("UPDATE Item "
                   "SET Current_Bid = Current_Bid + ?, Bid_Count = Bid_Count + 1, Current_Highest_Bidder = userid "
                   f"WHERE ItemID = ? AND Bid_Count = {actual_bidcount} "
                   "AND Current_Bid < (Current_Bid + ?) "  # adding negative & zero amounts
                   )  # check bid count at database level
            update = db.connection.cursor(prepared=True)
            update.execute(sql, (bid_increment, item_id, bid_increment,))
            db.disconnect()

            self.clear_item()
            return redirect("/item/{id}".format(id=item_id))

        self.clear_item()
        db.disconnect()
        return redirect("/item/{id}".format(id=item_id))
                                                                                                               
    def view_item(self, id, allow_to_bid=False):  # must be called before place_bid()
        self.item['expected-bidcount'] = None
        self.item['expected-bid'] = None

        allow_to_bid=allow_to_bid

        item_data = {'item': None}
        db = DB_Helper()
        sql = ("SELECT ItemID, UserID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date "
               "FROM Item "
               "WHERE ItemID=?")
        data = (id,)  # for prepared statement functionality. not sure if this is required.
        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, data)

        results = cursor.fetchall()

        for (ItemID, UserID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date) in results:
            item_data['item'] = [ItemID, UserID, Name.decode(), Image_Url.decode(), Status,
                                 Current_Bid.decode(), Bid_Count, Start_Date, End_Date]

        self.item['expected-bidcount'] = item_data['item'][6]  # user expectation set here and must be captured
        self.item['expected-bid'] = float(item_data['item'][5])

        db.disconnect(commit=True)
        return render_template("ItemForm.html", item_data=item_data, bid_allowed=allow_to_bid)

    def get_top_popular(self, limit=1):
        db = DB_Helper()
        sql = ("SELECT i.ItemID, i.UserID, "
               "i.Name, i.Image_Url, i.Status, "
               "i.Start_Bid, i.Current_Bid, i.Bid_Count, "
               "i.Start_Date, i.End_Date, "
               "u.FirstName, u.LastName, u.Location, i.Description "
               "FROM Item i, Users u "
               "WHERE u.UserID=i.UserID "
               "AND u.Type=1 AND i.Status='For_Sale' "
               "ORDER BY Bid_Count DESC LIMIT ?")

        data = (limit,)  # to satisfy execute method for prepared statement

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, data)
        results = cursor.fetchall()

        item_list = {'item': []}

        for (ItemID, UserID, Name, Image_Url, Status, Start_Bid, Current_Bid, Bid_Count, Start_Date, End_Date,
             FirstName, LastName, Location, Description) in results:
            item_list['item'].append([ItemID, UserID, Name.decode(), Image_Url.decode(), Status, Start_Bid,
                                      Current_Bid.decode(), Bid_Count, Start_Date, End_Date, FirstName.decode(), LastName.decode(),
                                      Location, Description.decode()])

        db.disconnect()
        return item_list

    def get_ending_soon(self, limit=1):
        db = DB_Helper()
        sql = ('SELECT ItemID, UserID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date '
               'FROM Item WHERE Status = "For_Sale" ORDER BY End_Date LIMIT ?')

        data = (limit,)  # to satisfy execute method for prepared statement

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql,data)
        results = cursor.fetchall()

        item_list = {'item': []}

        for (ItemID, UserID, Name, Image_Url, Status, Current_Bid, Bid_Count, Start_Date, End_Date) in results:
            item_list['item'].append(
                [ItemID, UserID, Name.decode(), Image_Url.decode(), Status, Current_Bid.decode(), Bid_Count,
                 Start_Date, End_Date])

        db.disconnect()
        return item_list

    def get_top_sellers(self, limit=1):
        db = DB_Helper()
        sql = ('SELECT Email, FirstName, LastName, Location, Password, Type, UserID '
               'FROM Users  WHERE Type = 1 Limit ?')


        data = (limit,)  # to satisfy execute method for prepared statement

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, data)
        results = cursor.fetchall()

        item_list = {'item': []}

        for (Email, FirstName, LastName, Location, Password, Type, UserID) in results:
            item_list['item'].append(
                [Email.decode(), UserID, Password, FirstName.decode(), LastName.decode(), Type, Location.decode()])

        db.disconnect()
        return item_list

    def get_user_type(self):
        """Uses the session to determine who user is: buyer, seller, or admin"""
        user_type = None

        if 'bidtown_session_key' in session and len(session['bidtown_session_key']) > 0:
            if type(session['bidtown_session_key'][0][0]) is int and session['bidtown_session_key'][0][6] == 0:
                user_type = "buyer"
            elif type(session['bidtown_session_key'][0][0]) is int and session['bidtown_session_key'][0][6] == 1:
                user_type = "seller"
            else:
                user_type = "admin"

        return user_type

    def get_user_id(self):
        """Obtains the user_id from the session cookie. Returns -1 if no user was found"""
        user_id = -1

        if 'bidtown_session_key' in session and len(session['bidtown_session_key']) > 0:
            if type(session['bidtown_session_key'][0][0]) is int:
                user_id = session['bidtown_session_key'][0][0]  # store the user id from session cookie
        return user_id
