from elasticsearch.exceptions import NotFoundError
import tools
import datetime
from conf import cnf


# offline task:order_count
def get_days_past_total_orders(n=1):
    # n means n days ago
    date = str(datetime.date.today() - datetime.timedelta(days=n)).replace('-', '')
    try:
        date_total_orders = tools.query_es_by_index_and_type(date, cnf.es_type_order_count, 'total_orders', 'pc_count',
                                                             'ios_count', 'android_count', 'money_sum', 'pc_money',
                                                             'ios_money', 'android_money')
    except NotFoundError:
        date_total_orders = {}
    return date_total_orders


# offline task:topn_products
def get_days_past_topn_products(n=1):
    date = str(datetime.date.today() - datetime.timedelta(days=n)).replace('-', '')
    try:
        date_topn_products = tools.query_es_by_index_and_type(date, cnf.es_type_topn_product, 'first_info',
                                                              'second_info', 'third_info')
    except NotFoundError:
        date_topn_products = {}
    return date_topn_products


# online task:today_order_count
def get_today_realtime_total_orders():
    today = str(datetime.date.today()).replace('-', '')
    today_total_orders = tools.query_es_by_aggs(cnf.es_index_today_order_count, today, 'sum', 'order_count',
                                                {'order_date': today})
    today_total_money = tools.query_es_by_aggs(cnf.es_index_today_order_count, today, 'sum', 'money_sum',
                                               {'order_date': today})
    return [today_total_orders, today_total_money]


# online task:today_topn_product
def get_today_realtime_topn_products():
    today = str(datetime.date.today()).replace('-', '')
    today_topn_products = tools.query_es_by_sort(cnf.es_index_today_topn_product, today, 1, None,
                                                 *({'date': {'order': 'desc'}},))
    if len(today_topn_products) == 0:
        return {}
    tmp = today_topn_products[0]['_source']
    topn_info = {'first': tmp['first_info'], 'second': tmp['second_info'], 'third': tmp['third_info']}
    return topn_info


# online task:today_reg
def get_today_realtime_reg():
    today = str(datetime.date.today()).replace('-', '')
    today_reg = tools.query_es_by_aggs(cnf.es_index_today_reg, today, 'sum', 'regCnt')
    return today_reg


# offline task:yestoday_reg
def get_days_past_reg(n=1):
    date = str(datetime.date.today() - datetime.timedelta(days=n)).replace('-', '')
    try:
        date_reg = tools.query_es_by_index_and_type(date, cnf.es_type_reg, 'regCnt')
    except NotFoundError:
        date_reg = {}
    return date_reg


# online task:today_dau
def get_today_dau():
    today = str(datetime.date.today()).replace('-', '')
    today_dau = tools.query_es_by_aggs(cnf.es_index_today_dau, today, 'max', 'dau')
    return today_dau


# offline task:yesterday_dau
def get_day_past_dau(n=1):
    date = str(datetime.date.today() - datetime.timedelta(days=n)).replace('-', '')
    try:
        date_dau = tools.query_es_by_index_and_type(date, cnf.es_type_reg, 'dau')
    except NotFoundError:
        date_dau = {}
    return date_dau


if __name__ == '__main__':
    # print(get_days_past_total_orders())
    # print(get_today_realtime_total_orders())
    # print(get_today_realtime_topn_products())
    print(get_today_realtime_reg())
    # print(get_days_past_topn_products())
