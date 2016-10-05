# code=utf-8

import os
import json
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options

from service.message import Message
from service.base import BaseHandler
from view.blogView import IndexHandler, BlogHandler
from view.uerView import LoginHandler
from view.messageView import MessageHandler
from view.uiModuleView import HeadUIModule

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):

        self.message = Message(self)

        handlers = [
            (r'/', IndexHandler),
            (r"/blog/([^/]+)", BlogHandler),
            (r'/login', LoginHandler),
            (r'/message/status', MessageHandler),
            (r".*", BaseHandler)
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

        # 启动时加载，后续数据全站缓存中，不在写回文本
        with open('api/user.json', 'r') as f:
            self.user_dict = json.load(f)

        with open('api/blog.json', 'r') as f:
            self.blog_dict = json.load(f)

        with open('api/message.json', 'r') as f:
            self.messages = json.load(f)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
