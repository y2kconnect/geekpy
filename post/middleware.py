import time


def simple_middleware(view_func):
    def wrap(request):
        print('hello simple_middleware')
        response = view_func(request)
        print('bye simple_middleware')
        return response
    return wrap


def request_rate(get_response):
    def wrap(request):
        # 1. session 不是只有登陆的情况下才能使用吗。
        # 2. 同局域网下的访问，只能通过 session 来区分不同用户

        # 访问时间
        # 第 1 次  100000.000
        # 第 2 次  100000.500
        # 第 3 次  100009.000

        history = request.session.get('req_history', [0, 0])  # 从 Session 里取出历史访问记录
        now = time.time()
        if (now - history[0]) < 1:  # 判断距离上上次访问的时间间隔是否小于 1 秒
            time.sleep(30)

        # 更新本次访问时间
        history.append(time.time())
        request.session['req_history'] = history[1:]

        return get_response(request)
    return wrap
