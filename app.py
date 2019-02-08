import functools

from flask import Flask, request, render_template
import time, tools, common, counts
from conf import cnf

app = Flask(__name__)


def get(path):
    '''
    Define decorator @get('/path')
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper

    return decorator


def post(path):
    '''
    Define decorator @post('/path')
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper

    return decorator


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', message=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))


@app.route('/signup.html', methods=['GET'])
@app.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    password_ensure = request.form['password_ensure']
    r = common.signin_index_valid(username, password, password_ensure)
    if r[0] == 0:
        return render_template('signup-ok.html', username=username, message=r[1])
    else:
        return render_template('signup.html', message=r[1])


@app.route('/login.html', methods=['GET'])
@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    r = common.login_index_valid(username, password)
    if r[0] == 0:
        return render_template('index.html', username=username)
    else:
        return render_template('login.html', message=r[1])


@app.route('/index/<username>', methods=['GET'])
def index(username):
    return render_template('index.html', username=username)


@app.route('/bankLoginOrSignup/<username>', methods=['GET'])
def login_or_signup_bank(username):
    return render_template('bank_login_signup.html', username=username)


@app.route('/signup_bank/<username>', methods=['POST'])
def signup_bank_form(username):
    cardno = request.form['cardno']
    password = request.form['password']
    password_ensure = request.form['password_ensure']
    r = common.signup_bank_valid(cardno, password, password_ensure, username)
    if r[0] == 0:
        return render_template('bank.html', cardno=cardno, signup_result=r[1], money=r[2], username=username)
    else:
        return render_template('bank_login_signup.html', signup_result=r[1], username=username)


@app.route('/login_bank/<username>', methods=['POST'])
def login_bank(username):
    cardno = request.form['cardno']
    password = request.form['password']
    r = common.login_bank_valid(cardno, password, username)
    if r[0] == 0:
        return render_template('bank.html', cardno=cardno, login_result=r[1], money=r[2], username=username)
    else:
        return render_template('bank_login_signup.html', cardno=cardno, login_result=r[1], username=username)


@app.route('/queryMoney/<cardno>', methods=['GET'])
def query_money(cardno):
    r = tools.select(cnf.t_wallet, *(2,), **{'0': cardno})[0]
    username = tools.select(cnf.t_rou_wallet, *(0,), **{'1': cardno})[0][0]
    return render_template('bank.html', cardno=cardno, money=r[0], username=username)


@app.route('/inMoney/<cardno>', methods=['POST'])
def in_money(cardno):
    money = request.form['inmoney']
    username = tools.select(cnf.t_rou_wallet, *(0,), **{'1': cardno})[0][0]
    r = common.add_money(cardno, money)
    return render_template('bank.html', cardno=cardno, money=r[1], username=username, in_result=r[2])


@app.route('/outMoney/<cardno>', methods=['POST'])
def out_money(cardno):
    money = request.form['outmoney']
    username = tools.select(cnf.t_rou_wallet, *(0,), **{'1': cardno})[0][0]
    r = common.add_money(cardno, money)
    return render_template('bank.html', cardno=cardno, money=r[1], username=username, out_result=r[2])


@app.route('/sendMoney/<cardno>', methods=['POST'])
def send_money(cardno):
    to_cardno = request.form['toCardno']
    money = request.form['sendmoney']
    username = tools.select(cnf.t_rou_wallet, *(0,), **{'1': cardno})[0][0]
    r = common.send_money(cardno, to_cardno, money)
    return render_template('bank.html', cardno=cardno, money=r[1], username=username, send_result=r[2])


@app.route('/go_shop/<username>', methods=['GET'])
def go_shop(username):
    return render_template('select_buy_sell.html', username=username)


@app.route('/shop_index/<username>', methods=['GET'])
def enter_customer(username):
    return render_template('shop_index.html', username=username)


@app.route('/seller_index/<username>', methods=['GET'])
def enter_seller(username):
    r = common.enter_seller_valid(username)
    if r[0] == 1:
        return render_template('seller_index.html', username=username)
    else:
        return render_template('select_buy_sell.html', username=username, login_result=r[1])


@app.route('/data_center/<username>', methods=['GET'])
def go_data_center(username):
    return render_template('data_index.html', username=username)


@app.route('/data/index/<username>', methods=['GET'])
def get_data_index(username):
    today_realtime_data = counts.get_today_realtime_total_orders()
    today_realtime_orders = int(today_realtime_data[0])
    today_realtime_money = float(today_realtime_data[1])
    today_topn_product = counts.get_today_realtime_topn_products()
    today_top1_product = today_topn_product.get('first', {'productid': None, 'sells': 0})
    today_top2_product = today_topn_product.get('second', {'productid': None, 'sells': 0})
    today_top3_product = today_topn_product.get('third', {'productid': None, 'sells': 0})
    yesterter_data = counts.get_days_past_total_orders()
    yesterday_orders = yesterter_data.get('total_orders', 0)
    yesterday_pc_count = yesterter_data.get('pc_count', 0)
    yesterday_ios_count = yesterter_data.get('ios_count', 0)
    yesterday_android_count = yesterter_data.get('android_count', 0)
    yesterday_pc_order_rate = round(yesterday_pc_count / (yesterday_orders + 0.01), 4)
    yesterday_ios_order_rate = round(yesterday_ios_count / (yesterday_orders + 0.01), 4)
    yesterday_android_order_rate = round(yesterday_android_count / (yesterday_orders + 0.01), 4)
    yesterday_money_sum = yesterter_data.get('money_sum', 0)
    yesterday_pc_money = yesterter_data.get('pc_money', 0)
    yesterday_ios_money = yesterter_data.get('ios_money', 0)
    yesterday_android_money = yesterter_data.get('android_money', 0)
    yesterday_pc_money_rate = round(yesterday_pc_money / (yesterday_money_sum + 0.01), 4)
    yesterday_ios_money_rate = round(yesterday_ios_money / (yesterday_money_sum + 0.01), 4)
    yesterday_android_money_rate = round(yesterday_android_money / (yesterday_money_sum + 0.01), 4)
    yesterday_topn_products_data = counts.get_days_past_topn_products(1)
    yesterday_top1_product = yesterday_topn_products_data.get("first_info", {'product_id': '', 'sells': 0})
    yesterday_top2_product = yesterday_topn_products_data.get("second_info", {'product_id': '', 'sells': 0})
    yesterday_top3_product = yesterday_topn_products_data.get("third_info", {'product_id': '', 'sells': 0})
    return render_template('data_index.html', username=username, today_realtime_orders=today_realtime_orders,
                           today_realtime_money=today_realtime_money,
                           yesterday_orders=yesterday_orders, yesterday_pc_order_rate=yesterday_pc_order_rate,
                           yesterday_ios_order_rate=yesterday_ios_order_rate,
                           yesterday_android_order_rate=yesterday_android_order_rate,
                           yesterday_money_sum=yesterday_money_sum, yesterday_pc_money_rate=yesterday_pc_money_rate,
                           yesterday_ios_money_rate=yesterday_ios_money_rate,
                           yesterday_android_money_rate=yesterday_android_money_rate,
                           yesterday_top1_productid=yesterday_top1_product.get("product_id"),
                           yesterday_top1_sells=yesterday_top1_product.get("sells"),
                           yesterday_top2_productid=yesterday_top2_product.get("product_id"),
                           yesterday_top2_sells=yesterday_top2_product.get("sells"),
                           yesterday_top3_productid=yesterday_top3_product.get("product_id"),
                           yesterday_top3_sells=yesterday_top3_product.get("sells"),
                           today_top1_productid=today_top1_product.get('productid'),
                           today_top1_sells=today_top1_product.get('sells'),
                           today_top2_productid=today_top2_product.get('productid'),
                           today_top2_sells=today_top2_product.get('sells'),
                           today_top3_productid=today_top3_product.get('productid'),
                           today_top3_sells=today_top3_product.get('sells'))


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
