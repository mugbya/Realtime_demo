# code = utf-8
import os
import binascii
import tornado.web
from service.base import BaseHandler


class IndexHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.web.authenticated
    def get(self):

        blog_list = []
        blog_dict = self.application.blog_dict

        for key in blog_dict.keys():
            blog = blog_dict[key]
            blog['id'] = key
            blog['comment_sum'] = len(blog['comment'])
            blog['username'] = self.application.user_dict[blog['author']]['username']
            blog_list.append(blog)

        return self.render('index.html', blog_list=blog_list)


class BlogHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, slug):
        '''
        返回文章详情
        :param slug:
        :return:
        '''
        blog_entry = None
        blog_dict = self.application.blog_dict

        message = self.request.arguments.get('message', None)
        if message:
            # 查看消息时,将当前消息置为已读
            message_id = message[0].decode('utf-8')
            self.application.message.read_message(message_id)

        if slug in self.application.blog_dict:
            blog_entry = blog_dict[slug]
            blog_entry.update({'id': slug})
            author = blog_dict[slug]['author']
            username = self.application.user_dict[author]['username']
            blog_entry.update({'username': username})

            comment_list = blog_dict[slug]['comment']
            for comment in comment_list:
                comment['username'] = self.application.user_dict[comment['author']]['username']

        return self.render("entry.html", blog=blog_entry)

    def post(self, slug, *args, **kwargs):
        '''
        保存评论, 监听消息
        :param args:
        :param kwargs:
        :return:
        '''
        user_info = self.current_user
        content = self.get_body_argument('content')

        blog = self.application.blog_dict[slug]
        # 保存评论
        self.application.blog_dict[slug]['comment'].append({'author': user_info['id'], "content": content})

        # 更新消息
        if blog['author'] != user_info['id']:
            # 他人评论需要推送消息
            message = {
                'id': binascii.hexlify(os.urandom(16)).decode("utf8"),
                'eventSource': slug,
                'eventType': 1,
                "data": blog['title'],
                "trigger": user_info['id'],
                "notice": blog['author'],
                "status": 0
            }
            self.application.message.add_message(message)

        return self.redirect('/blog/' + slug)
