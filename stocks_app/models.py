from flask_login import UserMixin
from stocks_app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    watch_list_stocks = db.relationship('Stock', secondary='stock_watch_list')
    watch_list_mfs = db.relationship('MutualFund', secondary='mf_watch_list')
    
class MutualFund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    desc = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Float(precision=2), nullable=False)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4), nullable=False)
    desc = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Float(precision=2), nullable=False)

stock_watch_list_table = db.Table('stock_watch_list',
    db.Column('stock_id', db.Integer, db.ForeignKey('stock.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

mf_watch_list_table = db.Table('mf_watch_list',
    db.Column('mutual_fund_id', db.Integer, db.ForeignKey('mutual_fund.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')))