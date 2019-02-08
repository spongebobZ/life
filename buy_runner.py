from common import buy
from conf import cnf
import tools
import threading
import random
import time

if __name__ == '__main__':
    rourou_list = list(map(lambda x: x[0], tools.select(cnf.t_rourou, *(0,))))
    product_list = list(map(lambda x: x[0], tools.select(cnf.t_product, *(0,))))
    client_list = ['pc', 'iOS', 'Android']
    product_cnt = len(product_list)
    while True:
        time.sleep(0.1)
        thread_list = []
        for i in rourou_list:
            buy_cnt = random.randint(1, product_cnt)
            thread_list.append(threading.Thread(target=buy, name=str(i), args=(
            i, client_list[random.randint(0, 2)], random.sample(product_list, buy_cnt))))
        for j in thread_list:
            j.start()
        for k in thread_list:
            k.join()