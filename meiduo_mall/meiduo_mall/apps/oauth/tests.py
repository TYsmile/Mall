from django.test import TestCase

# Create your tests here.

if __name__ == "__main__":
    # itsdangerous: 可以进行数据加密和解密
    # 安装: pip install itsdangerous

    # 加密
    from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer
    from itsdangerous import BadData
    # TJWSSerializer(secret_key='加解密密钥', expires_in='解密有效时间')
    # 假如密钥: 123abc
    # data = {
    #     'openid': 'AKKDKdk818289kKDOIkdka01929390'
    # }
    # serializer = TJWSSerializer(secret_key='123abc', expires_in=3600)
    #
    # res = serializer.dumps(data) # bytes
    # res = res.decode()
    # print(res)

    # 解密
    data = 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTUzNTI1MzEyMCwiaWF0IjoxNTM1MjQ5NTIwfQ.eyJvcGVuaWQiOiJBS0tES2RrODE4Mjg5a0tET0lrZGthMDE5MjkzOTAifQ.DeFTW0zwnDwU7jSCL8QCTQInpz01TGNb6cZHZHu502I'
    serializer = TJWSSerializer(secret_key='123abc', expires_in=3600)

    try:
        res = serializer.loads(data)
    except BadData as e:
        print(e)
    else:
        print(res)


# if __name__ == "__main__":
#     # 将python字典转化成一个查询字符串
#     # data = {
#     #     'id': 1,
#     #     'username': 'xiaohong'
#     # }
#     #
#     # # id=1&username=xiaohong
#     # from urllib.parse import urlencode
#     # res = urlencode(data)
#     # print(res)
#
#     # 将查询字符串转化为python字典
#     # query_str = 'a=1&b=2&c=3&c=4'
#     #
#     # from urllib.parse import parse_qs
#     # res = parse_qs(query_str) # 注意: key对应value是一个list
#     # print(res)
#
#     # 发送网络请求
#     # from urllib.request import urlopen
#     #
#     # req_url = 'http://api.meiduo.site:8000/mobiles/13155667788/count/'
#     # response = urlopen(req_url)
#     #
#     # # 获取响应数据
#     # res = response.read() # bytes
#     # res = res.decode()
#     # print(res)