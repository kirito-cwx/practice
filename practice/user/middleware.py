def simple_middleware(get_response):
    print('初始化中间件')

    def middleware(request):
        # 此处编写的代码会在每个请求处理视图前被调用。
        print('开始调用中间件')
        response = get_response(request)
        # 此处编写的代码会在每个请求处理视图之后被调用。
        print('结束调用中间件')

        return response

    return middleware


def my_middleware(get_response):
    print('init 被调用')

    def middleware(request):
        print('before request 被调用')
        response = get_response(request)
        print('after response 被调用')
        return response

    return middleware


def my_middleware2(get_response):
    print('init2 被调用')

    def middleware(request):
        print('before request 2 被调用')
        response = get_response(request)
        print('after response 2 被调用')
        return response

    return middleware
