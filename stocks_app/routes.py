from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
from datetime import date
from stocks_app.models import MutualFund, Stock, User
from stocks_app.forms import MutualFundForm, StockForm, LoginForm, SignUpForm, WatchForm, MutualFundForm2
from flask_login import login_required, login_user, logout_user, current_user
from stocks_app import b
from stocks_app import app, db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO

main = Blueprint("main", __name__)

@main.route('/')
def homepage():
    all_mutual_funds = MutualFund.query.all()
    all_stocks = Stock.query.all()
    return render_template('home.html', all_mutual_funds = all_mutual_funds, all_stocks = all_stocks)

@main.route('/new_mutual_fund', methods=['GET', 'POST'])
@login_required
def new_mutual_fund():
    form = MutualFundForm()

    if form.validate_on_submit():
        new_mutual_fund = MutualFund(
            name = form.name.data,
            desc = form.desc.data,
            value = form.value.data
        )
        db.session.add(new_mutual_fund)
        db.session.commit()
        flash('New mutual fund was created!')
        return redirect(url_for('main.mutual_fund_detail', mutual_fund_id = new_mutual_fund.id, mutual_fund = new_mutual_fund))

    return render_template('new_mutual_fund.html', form=form)

@main.route('/new_stock', methods=['GET', 'POST'])
@login_required
def new_stock():
    form = StockForm()

    if form.validate_on_submit():
        new_stock = Stock(
            name = form.name.data,
            desc = form.desc.data,
            value = form.value.data
        )
        db.session.add(new_stock)
        db.session.commit()
        flash('New stock was created!')

        return redirect(url_for('main.stock_detail', stock_id = new_stock.id))
    
    return render_template('new_stock.html', form=form)

@main.route('/mutual_fund/<mutual_fund_id>', methods=['GET', 'POST'])
@login_required
def mutual_fund_detail(mutual_fund_id):

    mutual_fund = MutualFund.query.get(mutual_fund_id)
    form = MutualFundForm(obj=mutual_fund)
    form2 = WatchForm()

    if form.validate_on_submit():
        mutual_fund.name = form.name.data,
        mutual_fund.desc = form.desc.data,
        mutual_fund.value = form.value.data
        db.session.commit()
        flash('Mutual fund was updated!')
        return redirect(url_for('main.mutual_fund_detail', mutual_fund = mutual_fund))
    
    mutual_fund = MutualFund.query.get(mutual_fund_id)
    return render_template('mutual_fund_detail.html', mutual_fund = mutual_fund, form = form, form2=form2)

@main.route('/stock/<stock_id>', methods=['GET', 'POST'])
@login_required
def stock_detail(stock_id):

    stock = Stock.query.get(stock_id)
    form = StockForm(obj=stock)
    form2 = WatchForm()
    form3 = MutualFundForm2()

    if form.validate_on_submit():
        stock.name = form.name.data
        stock.desc = form.desc.data
        stock.value = form.value.data

        db.session.commit()
        flash('Stock was updated!')
        return redirect(url_for('main.stock_detail', stock_id = stock.id))
    
    stock = Stock.query.get(stock_id)
    return render_template('stock_detail.html', stock=stock, form=form, form2=form2)

@main.route('/stock_watch_list_add/<stock_id>', methods = ['POST'])
@login_required
def stocks_watch_list_add(stock_id):
    user_current = current_user
    stock = Stock.query.get(stock_id)
    user_current.watch_list_stocks.append(stock)
    db.session.commit()
    flash('Stock added to watch list')
    return redirect(url_for('main.watch_list', watching_stocks=current_user.watch_list_stocks, watching_mfs=current_user.watch_list_mfs ))

@main.route('/mf_watch_list_add/<mutual_fund_id>', methods = ['POST'])
@login_required
def mfs_watch_list_add(mutual_fund_id):
    user_current = current_user
    mutual_fund = MutualFund.query.get(mutual_fund_id)
    user_current.watch_list_mfs.append(mutual_fund)
    db.session.commit()
    flash('Mutual fund added to watch list')
    return redirect(url_for('main.watch_list', watching_stocks=current_user.watch_list_stocks, watching_mfs=current_user.watch_list_mfs ))

@main.route('/watch_list')
@login_required
def watch_list():
    stocks = current_user.watch_list_stocks
    mfs = current_user.watch_list_mfs
    return render_template('watch_list.html', watching_stocks = stocks,  watching_mfs = mfs)

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = b.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and b.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

def create_image_file(xAxisData, yAxisData, xLabel, yLabel):
    """
    Creates and returns a line graph with the given data.
    Written with help from http://dataviztalk.blogspot.com/2016/01/serving-matplotlib-plot-that-follows.html
    """
    fig, _ = plt.subplots()
    plt.plot(xAxisData, yAxisData)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route('/graph/<current_price>')
def graph(current_price):
    """Creates a mock graph using the current price of the mutual fund or stock"""
    
    yAxisData = list()
    i = int(float(current_price))/30
    for _ in range(30):
        yAxisData.append(i)
        i += int(float(current_price))/30

    days = range(30)
    image = create_image_file(
        days,
        yAxisData,
        'Day',
        'Price'
    )
    return image