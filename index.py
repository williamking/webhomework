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
            target_users = []
            user_list.seek(0)
            for user in user_list:
                print(user)
                if (user == ""): continue
                information = user.split(',')
                if (information[0] == target_user[0]): continue
                print('1')
                if (information[1] == 'Female' and not('F' in target_user[5])): continue
                print('2')
                if (information[1] == 'Male' and not('M' in target_user[5])): continue
                print('3')
                value = 0
                if (information[2] >= target_user[6] and information[2] <= target_user[7]):
                    value += 1
                    print("well")
                if (information[4] == target_user[4]):
                    value += 1
                for c in information[3]:
                    if (c in target_user[3]): value += 1
                information.append(value)
                print(value)
                if (value >= 3): target_users.append(information)
        self.render('results.html', users=target_users)

class LoginHandler(BaseHandler):
    def get(self):
        self.render('index.html')

    def post(self):
        self.set_secure_cookie("username", self.get_argument("name"))
        valid = 1
        with open('./static/singles.txt', 'r+') as user_list:
            user_list.read()
            seek = self.get_arguments("seeking")
            if ("male" in seek and not("female" in seek)): seeking = 'M'
            if (not("male" in seek) and ("female" in seek)): seeking = 'F'
            if ("male" in seek and "female" in seek): seeking = 'MF'
            if (self.get_argument("name") == ""): valid = 0
            if (isinstance(self.get_argument("age"), int) == 0 or self.get_argument("age") < 0 or self.get_argument("age") > 99): valid = 0
            if (isinstance(self.get_argument("bottom-age"), int) == 0 or self.get_argument("bottom-age") < 0 or self.get_argument("bottom-age") > 99): valid = 0
            if (isinstance(self.get_argument("top-age"), int) == 0 or self.get_argument("top-age") < 0 or self.get_argument("top-age") > 99): valid = 0
            if (seek == []): valid = 0
            str = self.get_argument("personality-type")
            if (str[0] != 'I' and str[0] != 'E'): valid = 0
            if (str[1] != 'N' and str[0] != 'S'): valid = 0
            if (str[2] != 'F' and str[0] != 'T'): valid = 0
            if (str[3] != 'J' and str[0] != 'P'): valid = 0
            if (valid):
                user_list.write(self.get_argument("name"))
                user_list.write(',')
                user_list.write(self.get_argument("gender"))
                user_list.write(',')
                user_list.write(self.get_argument("age"))
                user_list.write(',')
                user_list.write(self.get_argument("personality-type"))
                user_list.write(',')
                user_list.write(self.get_argument("favorite-os"))
                user_list.write(',')
                user_list.write(seeking)
                user_list.write(',')
                user_list.write(self.get_argument("bottom-age"))
                user_list.write(',')
                user_list.write(self.get_argument("top-age"))
                user_list.write('\n')
        if (valid): self.redirect("/")
        else: self.redirect("/error") 

class ErrorHandler(BaseHandler):
    def get(self):
        self.render('error.html')

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
        handlers=[(r'/', MainHandler), (r'/login', LoginHandler), (r'/error', ErrorHandler)],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True, 
        **settings
    )

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()