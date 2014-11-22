import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        with open('./static/singles.txt', 'r') as user_list:
            target_user = ""
            for user in user_list:
                if (user == ''): continue
                if (user.split(',')[0] == self.current_user):
                    target_user = user.split(',')
        self.render('results.html', user=target_user)

class LoginHandler(BaseHandler):
    def get(self):
        self.render('index.html')

    def post(self):
        self.set_secure_cookie("username", self.get_argument("name"))
        with open('./static/singles.txt', 'w') as user_list:
            print(self.get_argument("top-age"))
            user_list.write(self.get_argument("name"))
        self.redirect("/")

if __name__ == "__main__":
    tornado.options.parse_command_line()

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "login_url": "/login",
        "xsrf_cookies": False
    }

    application = tornado.web.Application(
        handlers=[(r'/', MainHandler), (r'/login', LoginHandler)],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True, 
        **settings
    )

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()