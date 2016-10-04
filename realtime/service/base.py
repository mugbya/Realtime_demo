# code=utf-8

import binascii
import os
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    '''
    检测用户登陆
    '''
    # 类的静态变量用于保存登录信息, 存储的是token对应的user_id
    __TOKEN_LIST = {}

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def generate_token(self):
        while True:
            new_token = binascii.hexlify(os.urandom(16)).decode("utf8")
            if new_token not in self.__TOKEN_LIST:
                return new_token

    def on_login_success(self, new_token, user_id):
        self.set_cookie('_token', new_token)
        self.__TOKEN_LIST[new_token] = user_id

    def get_current_user(self):
        '''
        从cookie中读取token
        :return:
        '''
        token = self.get_cookie('_token')

        # 根据token得到绑定的用户id
        if token and token in self.__TOKEN_LIST:
            user_id = self.__TOKEN_LIST[token]
            user = self.application.user_dict[user_id]
            user.update({'id': user_id})
            return user

        # 没有找到就返回none, 表示该用户没有登录
        return None
