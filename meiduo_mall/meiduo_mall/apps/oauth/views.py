from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response

from oauth.utils import OAuthQQ
from oauth.exceptions import QQAPIError
from oauth.models import OAuthQQUser
from oauth.serializers import OAuthQQUserSerializer

from cart.utils import merge_cookie_cart_to_redis
# Create your views here.

# 获取logger
import logging
logger = logging.getLogger('django')


# GET /oauth/qq/user/?code=<code>
# class OAuthQQUserView(GenericAPIView):
class OAuthQQUserView(CreateAPIView):
    serializer_class = OAuthQQUserSerializer

    def post(self, request, *args, **kwargs):
        # 调用父类的post
        response = super().post(request, *args, **kwargs)

        # 补充购物车记录合并：调用合并购物车记录函数
        user = self.user
        merge_cookie_cart_to_redis(request, user, response)

        return response

    # def post(self, request):
    #     """
    #     绑定QQ登录用户:
    #     1. 获取参数并进行校验(参数完整性，手机号格式，短信验证是否正确，access_token是有效)
    #     2. 保存绑定QQ登录用户的信息，签发jwt token
    #         2.1 如果用户已注册，直接保存绑定信息
    #         2.2 如果用户未注册，先创建一个新用户，然后在保存绑定信息
    #     3. 返回应答
    #     """
    #     # 1. 获取参数并进行校验(参数完整性，手机号格式，短信验证是否正确，access_token是有效)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # 2. 保存绑定QQ登录用户的信息，签发jwt token
    #     #     2.1 如果用户已注册，直接保存绑定信息
    #     #     2.2 如果用户未注册，先创建一个新用户，然后在保存绑定信息
    #     serializer.save()
    #
    #     # 3. 返回应答
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        获取QQ登录用户的openid并进行处理:
        1. 获取code并进行校验(code必须传递)
        2. 获取QQ登录用户的openid
            2.1 根据code请求QQ服务器获取access_token
            2.2 根据access_token请求QQ服务器获取QQ登录用户的openid
        3. 根据openid进行处理
            3.1 如果openid已经绑定过本网站的用户，直接签发 jwt token，返回
            3.2 如果openid没有绑定过本网站的用户，对openid进行加密生成token，返回
        """
        # 1. 获取code并进行校验(code必须传递)
        code = request.query_params.get('code')

        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. 获取QQ登录用户的openid
        oauth = OAuthQQ()

        try:
            # 2.1 根据code请求QQ服务器获取access_token
            access_token = oauth.get_access_token(code)
            # 2.2 根据access_token请求QQ服务器获取QQ登录用户的openid
            openid = oauth.get_openid(access_token)
        except QQAPIError as e:
            logger.error(e)
            return Response({'message': 'QQ服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 3. 根据openid进行处理
        try:
            qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 3.2 如果openid没有绑定过本网站的用户，对openid进行加密生成token，返回
            token = OAuthQQ.generate_save_user_token(openid)
            return Response({'access_token': token})
        else:
            # 3.1 如果openid已经绑定过本网站的用户，直接签发 jwt token，返回
            user = qq_user.user
            # 由服务器签发一个jwt token，保存用户身份信息
            from rest_framework_jwt.settings import api_settings

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            # 生成载荷信息(payload)
            payload = jwt_payload_handler(user)
            # 生成jwt token
            token = jwt_encode_handler(payload)

            # 返回
            resp = {
                'user_id': user.id,
                'username': user.username,
                'token': token
            }

            # 补充购物车记录合并：调用合并购物车记录函数
            response = Response(resp)
            merge_cookie_cart_to_redis(request, user, response)

            return response


# GET /oauth/qq/authorization/?next=<url>
class OAuthQQURLView(APIView):
    def get(self, request):
        """
        获取QQ登录网址:
        1. 获取参数next
        2. 组织QQ登录url地址和参数
        3. 返回QQ登录网址
        """
        # 1. 获取参数next
        next = request.query_params.get('next', '/')

        # 2. 组织QQ登录url地址和参数
        oauth = OAuthQQ(state=next)
        login_url = oauth.get_login_url()

        # 3. 返回QQ登录网址
        return Response({'login_url': login_url})
