# code=utf-8

import os
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options

from service.message import Message
from view.blogView import IndexHandler
from view.uerView import LoginHandler
from view.uiModuleView import HeadUIModule

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):

        self.message = Message()

        handlers = [
            (r'/', IndexHandler),
            (r'/login', LoginHandler)
        ]

        settings = dict(
            blog_title=u"Tornado Blog",
            template_path=os.path.join(os.path.dirname(__file__), "webContent/templates"),
            static_path=os.path.join(os.path.dirname(__file__), "webContent/static"),
            # ui_modules=my_uimodules,
            ui_modules={'Head': HeadUIModule},
            # xsrf_cookies=True,
            cookie_secret='1111111111111111111111111111111111111111111111111',
            login_url='/login',
            debug=True,
        )

        super(Application, self).__init__(handlers, **settings)

        self.user_list = {
            '1': {'username': 'pom', 'password': 'pom'},
            '2': {'username': 'nash', 'password': 'nash'}
        }

        self.blog_list = [
            {'id': 1, 'title': u'雨滴', 'content': u'我听见下课钟声响起', 'user': 'admin',
             'comment': [{'user': 'mugbya', 'content': u'测试'}]}]
        self.comment_list = []

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
