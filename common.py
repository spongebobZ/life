import re, random, time, datetime
import tools
from conf import cnf


def signin_index_valid(username, password, password_ensure):
    if username.strip() == '':
        r = [-1, '名字不能为空！(￣ε(#￣)☆╰╮(￣▽￣///)']
    elif len(tools.select(cnf.t_rourou, **{'1': username})) != 0:
        r = [-1, '此名字已被别的肉使用！(￣ε(#￣)☆╰╮(￣▽￣///)']
    elif not re.match('\d{4}$', password) or int(password) % 1111 == 0:
        r = [-1, '密码仅限制为4位数字，且不能全部一样！(￣ε(#￣)☆╰╮(￣▽￣///)']
    elif password != password_ensure:
        r = [-1, '两次密码输入不一致(￣ε(#￣)☆╰╮(￣▽￣///)']
    else:
        record = tools.select(cnf.t_rourou, *(0,))
        rou_id = int(record[-1][0]) + 1 if len(record) > 0 else 0
        tools.insert(cnf.t_rourou, '%s,%s,%s' % (str(rou_id), username, password))
        r = [0, '恭喜注册成功♪(^∇^*)']
    return r


def login_index_valid(username, password):
    if len(tools.select(cnf.t_rourou, **{'1': username, '2': password})) == 1:
        r = [0, '登录成功O(∩_∩)O']
    else:
        r = [-1, '账号密码错误(；′⌒`)']
    return r


def random_cardno():
    while True:
        r = random.randint(10000000, 99999999)
        if len(tools.select(cnf.t_wallet, **{'0': r})) == 0:
            return r


def signup_bank_valid(cardno, password, password_ensure, username):
    if cardno.strip() == '':
        r = [-1, '卡号不能为空！(￣ε(#￣)☆╰╮(￣▽￣///)']
    elif len(tools.select(cnf.t_wallet, **{'1': cardno})) != 0:
        r = [-1, '此卡号已被别的肉使用！(￣ε(#￣)☆╰╮(￣▽￣///)']
    elif not re.match('\d{4}$', password) or int(password) % 1111 == 0:
        r = [-1, '密码仅限制为4位数字，且不能全部一样！(￣ε(#￣)☆╰╮(￣▽￣///)']
    elif password != password_ensure:
        r = [-1, '两次密码输入不一致(￣ε(#￣)☆╰╮(￣▽￣///)']
    else:
        tools.insert(cnf.t_wallet, '%s,%s,%s' % (str(cardno), password, '0'))
        tools.insert(cnf.t_rou_wallet, '%s,%s' % (username, cardno))
        r = [0, '恭喜注册成功♪(^∇^*)', 0]
    return r


def login_bank_valid(cardno, password, username):
    record = tools.select(cnf.t_wallet, **{'0': cardno, '1': password})
    record_user_wallet = tools.select(cnf.t_rou_wallet, **{'0': username, '1': cardno})
    if len(record) == 1 and len(record_user_wallet) == 1:
        r = [0, '登录成功O(∩_∩)O', record[0][2]]
    elif len(record) != 1:
        r = [-1, '账号密码错误(；′⌒`)']
    else:
        r = [-2, '卡号是别的肉的(；′⌒`)']
    return r


def add_money(cardno, money):
    # r 0 成功,-1格式错误
    old = int(tools.select(cnf.t_wallet, *(2,), **{'0': cardno})[0][0])
    r = [-1, old, '存钱失败(；′⌒`)']
    if re.match(r'^\d+$', money):
        money = int(money)
        tools.update(cnf.t_wallet, {'2': str(old + money)}, **{'0': cardno})
        r = [0, str(old + 9 + money), '存钱成功( •̀ ω •́ )y']
    return r


def reduce_money(cardno, money):
    # r 0 成功,-1格式错误,-2余额不足
    old = int(tools.select(cnf.t_wallet, *(2,), **{'0': cardno})[0][0])
    r = [-1, old, '取钱失败(；′⌒`)']
    if re.match(r'^\d+$', money):
        money = int(money)
        if money > old:
            r = [-2, old, '余额不足(；′⌒`)']
        else:
            tools.update(cnf.t_wallet, {'2': str(old - money)}, **{'0': cardno})
            r = [0, str(old - money), '取钱成功( •̀ ω •́ )y']
    return r


def send_money(cardno, tocardno, money):
    # r 0 成功,-1格式错误,-2余额不足,-3 收款方账号不存在,-4 收款方账号为自己
    old = int(tools.select(cnf.t_wallet, *(2,), **{'0': cardno})[0][0])
    r = [-1, old, '转钱失败(；′⌒`)']
    if re.match(r'^\d+$', money):
        money = int(money)
        if money > old:
            r = [-2, old, '余额不足(；′⌒`)']
        elif len(tools.select(cnf.t_wallet, **{'0': tocardno})) == 0:
            r = [-3, old, '收钱肉账号错误(；′⌒`)']
        elif cardno == tocardno:
            r = [-4, old, '多么闲着无聊才会转钱给自己Σ(っ °Д °;)っ']
        else:
            to_old = int(tools.select(cnf.t_wallet, *(2,), **{'0': tocardno})[0][0])
            tools.update(cnf.t_wallet, {'2': str(old - money)}, **{'0': cardno})
            tools.update(cnf.t_wallet, {'2': str(to_old + money)}, **{'0': tocardno})
            new = tools.select(cnf.t_wallet, *(2,), **{'0': cardno})[0][0]
            r = [0, new, '转钱成功( •̀ ω •́ )y']
    return r


def enter_seller_valid(username):
    # r 0 未成为seller, 1 已成为seller
    r = [0, '你还没有成为商人(╬▔皿▔)凸']
    if len(tools.select(cnf.t_seller, **{'0': username})) != 0:
        r = [1, '欢迎尊贵的商人(｡･∀･)ﾉﾞ嗨']
    return r


def buy(user_id, client, product_list):
    order_id = str(time.time()).replace('.', '')[:13]
    date = datetime.datetime.now()
    order_dow = str(date.weekday())
    day_for_current_month = str(date.day)
    order_hour_of_day = date.hour
    for i, product in enumerate(product_list):
        tools.insert(cnf.t_orders, '%s,%s,%s,%s,%s,%s,%s' % (
        order_id, str(user_id), str(i), order_hour_of_day, order_dow, day_for_current_month, client))
        tools.insert(cnf.t_product_prior, '%s,%s,%s' % (order_id, str(product), str(i)))
