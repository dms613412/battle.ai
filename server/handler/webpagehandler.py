import tornado.web
import server.debugger as logging


class WebServer(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class TestHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        logging.debug(chunk)
        pass

    def get(self, *args, **kwargs):
        print(str(args))
        print(str(kwargs))

        self.render("main.html")

pass
