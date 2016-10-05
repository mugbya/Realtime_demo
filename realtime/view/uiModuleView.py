# code=utf-8


from service.message import Message
from service.base import BaseHandler
import tornado.web


class HeadUIModule(tornado.web.UIModule, BaseHandler):
    def render(self, *args, **kwargs):
        username = u'游客'
        messages, unread = [], 0
        if self.current_user:
            username = self.current_user['username']
            messages, unread = Message(self.handler.application, self.request).get_message_by_user(self.current_user)
        return self.render_string('modules/head.html', username=username, messages=messages, unread=unread)
