import tornado.web,tornado.ioloop
import motor
import pymongo           
import json
from tornado.escape import json_encode,json_decode
           
class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
	#async_client=AsyncHTTPClient()
        """
	self.write('''
        <form method="post">
            <input type="text" name="msg" \n >
            <input type="submit">
        </form>''')
	
	"""
	output= self.settings['db'].tasks.find()
	tasks= []
	while(yield output.fetch_next):
            task = output.next_object()
	    tasks.append({'name':task['task']})
	self.set_header("content-type","application/json")
	self.write(json_encode(tasks))
	self.finish()

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
	task=self.get_argument('task')
	yield self.settings['db'].tasks.insert({'task':task})
        self.finish()
	
db=motor.MotorClient().test
 
application=tornado.web.Application(
    [
	(r'/todo',MainHandler)
    ],
    db=db
)
application.listen(8000)
tornado.ioloop.IOLoop.instance().start()

