from django.core.cache import cache
from redis import Redis

from post.models import Post

rds = Redis('127.0.0.1', 6379, db=1)


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


def get_post_rank(n):
    '''获取浏览量前 10 的文章列表'''

    # rank 的数据结构
    # [
    #     (b'3', 13.0),
    #     (b'9', 12.0),
    #     (b'1', 8.0),
    #     (b'7', 3.0),
    #     (b'0', 2.0)
    # ]
    top10 = []
    rank = rds.zrevrange('ReadRank', 0, n - 1, withscores=True)

    # 低效的方式
    # for str_id, count in rank:
    #     post_id = int(str_id)
    #     post = Post.objects.get(id=post_id)
    #     top10.append([post, int(count)])

    # 高效方式
    post_id_list = [int(str_id) for str_id, _ in rank]
    posts = Post.objects.in_bulk(post_id_list)  # 格式: {post_id_1: Post(1), post_id_7: Post(7)}
    top10 = [[posts[int(post_id)], int(count)] for post_id, count in rank]
    # for post_id, count in rank:
    #     post = posts[int(post_id)]
    #     count = int(count)
    #     top10.append([post, count])

    return top10
