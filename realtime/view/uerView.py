# code=utf-8

from service.base import BaseHandler


class LoginHandler(BaseHandler):
    '''
    处理登陆
    '''
    def get(self):
        next_url = self.request.arguments.get('next', '/')
        if isinstance(next_url, list):
            next_url = next_url[0].decode('utf-8')
        return self.render('login.html', next=next_url)

    def post(self):
        username = self.get_body_argument('username')
        password = self.get_body_argument('password')

        # 检测用户名和密码
        login_user = None
        for user in self.application.user_list:
            if username == self.application.user_list[user]['username']:
                login_user = user
                break
        if not login_user:
            return self.finish('用户名或密码错误')

        if password != self.application.user_list[login_user]['password']:
            return self.finish('用户名或密码错误')

        # 一个token对应一个已经登录的用户
        new_token = self.generate_token()
        self.on_login_success(new_token, login_user)

        next_url = self.get_body_argument('next', None)
        if next_url:
            print(next_url)
            return self.redirect(next_url)
        return self.finish('ok')