import re
def jwt_response_payload_handler(token, user=None, request=None):
    """自定义jwt登录视图响应数据"""
    return {
        'user_id': user.id,
        'username': user.username,
        'token': token
    }


# 自定义Django认证系统后端类
from django.contrib.auth.backends import ModelBackend
from users.models import User


def get_user_by_account(account):
    """
    account: 用户名或手机号
    """
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            # 根据手机号查询用户
            user = User.objects.get(mobile=account)
        else:
            # 根据用户名查询用户
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        user = None

    return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        username: 可能是用户名或手机号
        """
        # 根据用户名或手机号查询用户的信息
        user = get_user_by_account(username)

        # 如果用户存在，检验密码是否正确
        if user and user.check_password(password):
            return user
