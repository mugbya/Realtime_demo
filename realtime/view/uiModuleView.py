# code=utf-8


from service.base import BaseHandler
import tornado.web


class HeadUIModule(tornado.web.UIModule):

    def render(self, *args, **kwargs):
        return self.render_string('modules/head.html', username='nash')