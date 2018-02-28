from django.core.cache import cache


def page_cache(timeout):
    '''页面缓存'''
    def wrap1(view_func):
        def wrap2(request, *args, **kwargs):
            # 只缓存 GET 请求
            if request.method == 'GET':
                key = 'PageCache:%s' % request.get_full_path()  # 构造 key
                response = cache.get(key)
                if response is None:
                    print('get response from view: %s' % key)
                    response = view_func(request, *args, **kwargs)
                    cache.set(key, response, timeout)  # 设置过去时间，让旧缓存自动失效
                return response
            else:
                return view_func(request, *args, **kwargs)
        return wrap2
    return wrap1
