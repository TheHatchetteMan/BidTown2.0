from flask import request
from DB_Helper import DB_Helper

class BidManager:
    #static/shared data

    def __init__(self):
        self.single_item_result = []


    def place_bid(self):
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
            return "You should be redirected to the newly updated bid data that shows the winning bid is you!"

        db.disconnect()
        return "Your bid data is outdated. You need to be redirected to the new bid data for this item."