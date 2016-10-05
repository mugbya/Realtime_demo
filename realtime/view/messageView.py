# code=utf-8

import tornado.websocket


class MessageHandler(tornado.websocket.WebSocketHandler):

    def open(self, *args, **kwargs):
        self.application.message.register(self.callback)

    def on_close(self):
        self.application.message.un_register(self.callback)

    def callback(self, result):
        # 只处理新增的消息，
        self.write_message({'message': result[0][-1], 'unread': result[1]})

