# ----- Developer: Hunter Hatchette ----- #

from flask import request, render_template, redirect
from DB_Helper import DB_Helper


class AccountManager:
    # static/shared data

    def __init__(self):
        self.item = {'expected-bidcount': None, 'expected-bid': None}

    def clear_item(self):
        self.item['expected-bid'] = None
        self.item['expected-bidcount'] = None

    def view_active_items(self, limit=1):
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
