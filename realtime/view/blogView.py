# code = utf-8
import json
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
            for message in self.application.messages:
                if message_id == message['id']:
                    message['status'] = 1

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
        保存评论
        :param args:
        :param kwargs:
        :return:
        '''
        user_info = self.current_user
        content = self.get_body_argument('content')

        self.application.blog_dict[slug]['comment'].append({'author': user_info['id'], "content": content})

        return self.redirect('/blog/' + slug)