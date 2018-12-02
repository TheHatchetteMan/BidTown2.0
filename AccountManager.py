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
