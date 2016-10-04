# code=utf-8


from service.message import Message
import tornado.web


class HeadUIModule(tornado.web.UIModule):

    def render(self, *args, **kwargs):
        username = u'游客'
        if self.current_user:
            username = self.current_user['username']
            # message = Message().getMessagesByUser(user_name)
        return self.render_string('modules/head.html', username=username)