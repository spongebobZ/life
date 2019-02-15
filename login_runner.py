import random
import time
import tools
from conf import cnf
from common import login_index_valid, logout_index
import threading

# 在线用户队列，eg：{'brr':[10,60]}，表示brr用户设置的在线时长为60s，剩余下线时间为10s
online_queue = {}
lock = threading.Lock()


def login_queue():
    all_acounts = list(map(lambda x: x[0], tools.select(cnf.t_rourou, *(1,))))
    acount_cnt = len(all_acounts)
    while True:
        login_cnt = random.randint(0, acount_cnt // 3)
        login_acounts = random.sample(all_acounts, login_cnt)
        tmp_queue = dict(online_queue)
        for i in login_acounts:
            if i not in tmp_queue:
                t = random.randint(30, 100)
                tmp_queue[i] = [t, t]
                login_index_valid(i, '0000')
        # for j in tmp_queue:
        #     print('%s login' % j)
        change_queue(tmp_queue)
        time.sleep(random.randint(10, 60))


def run_queue():
    while True:
        time.sleep(1)
        tmp_queue = dict(online_queue)
        del_keys = []
        for k, v in tmp_queue.items():
            if v[0] <= 0:
                del_keys.append(k)
                # print('%s logout' % k)
                logout_index(k)
            else:
                v[0] -= 1
        for i in del_keys:
            tmp_queue.pop(i)
        change_queue(tmp_queue)


def change_queue(d):
    lock.acquire()
    global online_queue
    try:
        online_queue = d
        del d
    finally:
        lock.release()


if __name__ == '__main__':
    t_login = threading.Thread(target=login_queue, name='login thread')
    t_run = threading.Thread(target=run_queue, name='run time thread')
    t_login.start()
    t_run.start()
    t_login.join()
    t_run.join()
