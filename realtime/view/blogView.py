# code = utf-8

import tornado.web
from service.base import BaseHandler


class IndexHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.web.authenticated
    def get(self):
        return self.render('index.html')

