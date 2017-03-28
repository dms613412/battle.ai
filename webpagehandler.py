import io
from tkinter import Image

import markdown as markdown
import tornado.web
from tornado import gen
import server.debugger as logging
import os
import bcrypt
import concurrent.futures
import os.path
import re
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

from tornado.options import define, options

from server.conf.conf_reader import ConfigReader

define("port", default=9002, help="run on the given port", type=int)

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


# sample code
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/(backosori.jpg)", tornado.web.StaticFileHandler, {'path':'/templates/'}),
            # (r"/archive", ArchiveHandler),
            # (r"/feed", FeedHandler),
            # (r"/entry/([^/]+)", EntryHandler),
            (r"/mypage", MyPageHandler),
            (r"/playground", PlaygroundHandler),
            # (r"/compose", ComposeHandler),
            # (r"/auth/create", AuthCreateHandler),
            # (r"/auth/login", AuthLoginHandler),
            # (r"/auth/logout", AuthLogoutHandler),
        ]
        settings = dict(
            blog_title=u"Battle.ai",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # ui_modules={"Entry": Entry},
            xsrf_cookies=True,
            # cookie_secret="secret_code",
            login_url="/auth/login",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        # Have one global connection to the blog DB across all handlers
        # self.db = torndb.Connection(
        #     host=options.mysql_host, database=options.mysql_database,
        #     user=options.mysql_user, password=options.mysql_password)

        self.maybe_create_tables()

    def maybe_create_tables(self):
        pass
        # try:
        #     self.db.get("SELECT COUNT(*) from entries;")
        # except MySQLdb.ProgrammingError:
        #     subprocess.check_call(['mysql',
        #                            '--host=' + options.mysql_host,
        #                            '--database=' + options.mysql_database,
        #                            '--user=' + options.mysql_user,
        #                            '--password=' + options.mysql_password],
        #                           stdin=open('schema.sql'))


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        #return self.application.db
        pass

    def get_current_user(self):
        # user_id = self.get_secure_cookie("blogdemo_user")
        # if not user_id:
        #     return None
        # return self.db.get("SELECT * FROM authors WHERE id = %s", int(user_id))
        pass

    def any_author_exists(self):
        # return bool(self.db.get("SELECT * FROM authors LIMIT 1"))
        pass


class HomeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        #print(self.db)
        self.render("main.html")


class MyPageHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("sample.html")


class PlaygroundHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("index.html")


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    print("******************* Battle.AI operate *******************")
    print("                     ...... Created By GreedyOsori ......\n")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()