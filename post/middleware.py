import time

from django.core.cache import cache


def simple_middleware(view_func):
    def wrap(request):
        print('hello simple_middleware')
        response = view_func(request)
        print('bye simple_middleware')
        return response
    return wrap


def request_rate(get_response):
    def wrap(request):
        # 1. session 只有登陆的情况下才能使用吗？
        # 2. 通过 IP 记录的话，怎么解决同局域网下的访问

        # 访问时间
        # 第 1 次  100000.000
        # 第 2 次  100000.500
        # 第 3 次  100009.000

        key = 'RequestTime-%s' % request.META['REMOTE_ADDR']
        history = cache.get(key, [0, 0])  # 取出历史访问记录
        now = time.time()
        if (now - history[0]) < 1:  # 判断距离上上次访问的时间间隔是否小于 1 秒
            time.sleep(2)

        # 跟新本次访问时间
        history.append(time.time())
        cache.set(key, history[1:])

        return get_response(request)
    return wrap
