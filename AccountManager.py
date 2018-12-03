# ----- Developer: Hunter Hatchette ----- #

from flask import request, render_template, redirect, session
from DB_Helper import DB_Helper


class AccountManager:
    # static/shared data

    def __init__(self):
        self.item = {'expected-bidcount': None, 'expected-bid': None}

    def clear_item(self):
        self.item['expected-bid'] = None
        self.item['expected-bidcount'] = None

    def view_active_items(self, limit=1):
        db = DB_Helper()

        if 'bidtown_session_key' in session and len(session['bidtown_session_key']) > 0:
            userid = [{session['bidtown_session_key'][0][0]}]

        sql = ("SELECT i.ItemID, i.UserID, i.ClassID, "
               "i.Name, i.Image_Url, i.Status, "
               "i.Start_Bid, i.Current_Bid, i.Bid_Count, "
               "i.Start_Date, i.End_Date, "
               "u.FirstName, u.LastName, u.Location "
               "FROM Item i, Users u "
               "WHERE u.UserID=i.UserID "
               "AND u.Type=1 AND i.Status='For_Sale' "
               "AND i.UserID=2 "
               "ORDER BY Bid_Count DESC LIMIT ?")

        data = (limit,)  # to satisfy execute method for prepared statement

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, data)
        results = cursor.fetchall()

        item_list = {'item': []}

        for (ItemID, UserID, ClassID, Name, Image_Url, Status, Start_Bid, Current_Bid, Bid_Count, Start_Date, End_Date,
             FirstName, LastName, Location) in results:
            item_list['item'].append([ItemID, UserID, ClassID, Name.decode(), Image_Url.decode(), Status, Start_Bid,
                                      Current_Bid.decode(), Bid_Count, Start_Date, End_Date, FirstName, LastName,
                                      Location])

        db.disconnect()
        return item_list

    def view_sold_items(self, limit=1):
        db = DB_Helper
        sql = ()

        data = (limit,)  # to satisfy execute method for prepared statement

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, data)
        results = cursor.fetchall()

        item_list = {'item': []}

        for (ItemID, UserID, ClassID, Name, Image_Url, Status, Start_Bid, Current_Bid, Bid_Count, Start_Date, End_Date,
             FirstName, LastName, Location) in results:
            item_list['item'].append([ItemID, UserID, ClassID, Name.decode(), Image_Url.decode(), Status, Start_Bid,
                                      Current_Bid.decode(), Bid_Count, Start_Date, End_Date, FirstName, LastName,
                                      Location])

        db.disconnect()
        return item_list

    def view_watching_items(self, limit=1):
        db = DB_Helper
        sql = ()

        data = (limit,)  # to satisfy execute method for prepared statement

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, data)
        results = cursor.fetchall()

        item_list = {'item': []}

        for (ItemID, UserID, ClassID, Name, Image_Url, Status, Start_Bid, Current_Bid, Bid_Count, Start_Date, End_Date,
             FirstName, LastName, Location) in results:
            item_list['item'].append([ItemID, UserID, ClassID, Name.decode(), Image_Url.decode(), Status, Start_Bid,
                                      Current_Bid.decode(), Bid_Count, Start_Date, End_Date, FirstName, LastName,
                                      Location])

        db.disconnect()
        return item_list

    def view_bought_items(self, limit=1):
        db = DB_Helper
        sql = ()

        data = (limit,)  # to satisfy execute method for prepared statement

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, data)
        results = cursor.fetchall()

        item_list = {'item': []}

        for (ItemID, UserID, ClassID, Name, Image_Url, Status, Start_Bid, Current_Bid, Bid_Count, Start_Date, End_Date,
             FirstName, LastName, Location) in results:
            item_list['item'].append([ItemID, UserID, ClassID, Name.decode(), Image_Url.decode(), Status, Start_Bid,
                                      Current_Bid.decode(), Bid_Count, Start_Date, End_Date, FirstName, LastName,
                                      Location])

        db.disconnect()
        return item_list

    def view_bid_items(self, limit=1):
        db = DB_Helper
        sql = ()

        data = (limit,)  # to satisfy execute method for prepared statement

        cursor = db.connection.cursor(prepared=True)
        cursor.execute(sql, data)
        results = cursor.fetchall()

        item_list = {'item': []}

        for (ItemID, UserID, ClassID, Name, Image_Url, Status, Start_Bid, Current_Bid, Bid_Count, Start_Date, End_Date,
             FirstName, LastName, Location) in results:
            item_list['item'].append([ItemID, UserID, ClassID, Name.decode(), Image_Url.decode(), Status, Start_Bid,
                                      Current_Bid.decode(), Bid_Count, Start_Date, End_Date, FirstName, LastName,
                                      Location])

        db.disconnect()
        return item_list

    def get_current_user(self):
        db = DB_Helper
        userID = {{session['bidtown_session_key'][0][0]}}
        return userID
