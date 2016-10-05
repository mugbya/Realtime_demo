# code = utf-8
import json
from service.base import BaseHandler


class Message(BaseHandler):
    '''
    定义消息类
    '''
    callables = []

    def register(self, callback):
        '''
        消息注册
        :param callback:
        :return:
        '''
        self.callables.append(callback)

    def un_register(self, callback):
        self.callables.remove(callback)

    def add_message(self, message):
        self.application.messages.append(message)

        user_dict = self.application.user_dict

        user = user_dict.get(message['notice'], {})
        user.update({'id': message['notice']})

        self.notify_callbacks(user)

    def read_message(self, message):
        pass

    def notify_callbacks(self, user):
        '''
        通告消息
        :param user:
        :return:
        '''
        for callback in self.callables:
            callback(self.get_message_by_user(user))

    def get_message_by_user(self, user):
        '''
        获取指定用户消息列表
        :param user:
        :return:
        '''
        user_dict = self.application.user_dict

        message_list = []
        unread = 0
        for message in self.application.messages:
            if user['id'] == message['notice']:
                if not message['status']:
                    unread += 1
                user = user_dict.get(message['trigger'], {})
                message['username'] = user['username']
                message_list.append(message)

        return message_list, unread