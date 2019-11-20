import tornado.ioloop
import tornado.web
import asyncio
import time
import threading


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        print("Thread: ", threading.current_thread())
        self.write("start at: "+str(time.ctime()+"\n"))
        await asyncio.sleep(10)
        self.write("finish at: "+str(time.ctime()+"\n"))
        self.finish()
        print("someone get me")


class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!!!!!!")
    pass


class staticRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("testfile.html")
    pass


class queryStringRequestHandler(tornado.web.RequestHandler):
    def get(self):
        n = int(self.get_argument("n"))
        r = "odd" if n % 2 else "even"
        self.write("the number " + str(n) +
                   " is" + r)
    pass


class resourceRequestHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.write("Querying tweet with id:" + id)
    pass



if __name__ == "__main__":
    print('hello')
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/blog", staticRequestHandler),
        (r"/isEven", queryStringRequestHandler),
        (r"/tweet/(.*)", resourceRequestHandler),  # regular expression
    ])
    print('hello2')
    application.listen(8888)  # you need to access localhost:8888 to see
    print('hello3')
    tornado.ioloop.IOLoop.current().start()  # infinite loop
    print('hello4')
