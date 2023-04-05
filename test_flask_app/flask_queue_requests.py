from flask import Flask, current_app, request
import time

import logging

# 1. Create logger object
logger = logging.getLogger('myproject')

# 2. Set logging level
logger.setLevel(logging.INFO)

# 3. Configure handler(s)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

# 4. Log messages throughout the code
logger.info('This is an information message')
logger.warning('This is a warning message')
logger.error('This is an error message')

# app = Flask(__name__)

# class MyFlaskApp(object):
#     def __init__(self):
#         self.app = app
#         self.register_routes()
        
#     def register_routes(self):
#         self.app.add_url_rule('/', view_func=self.index)
#         self.app.add_url_rule('/about', view_func=self.about)
        
#     def index(self):
#         return 'Welcome to my Flask app!'
    
#     def about(self):
#         return 'This is a simple Flask app built using object-oriented approach.'
    
# if __name__ == '__main__':
#     my_app = MyFlaskApp()

#     with my_app.app.app_context():
#         current_app.test = 'my variable'

#     my_app.app.run(debug=True)


from flask import Flask, current_app, request
import time
from celery import Celery

max_concurrent_requests = 3
active_requests = 0

class FlaskAppWrapper(object):

    def __init__(self, app, **configs):
        self.app = app

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)
    
    def hello_world(self):
        time.sleep(5)
        return "Hello, world!"
    
    def run(self, **kwargs):
        self.app.run(**kwargs)


if __name__ == "__main__":

    flask_app = Flask(__name__)
    #Configure the redis server
    flask_app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    flask_app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    # celery = Celery(flask_app.name, broker='amqp://guest@localhost//')
    celery = Celery(flask_app.name, broker=flask_app.config['CELERY_BROKER_URL'])
    celery.conf.update(flask_app.config)

    @celery.task
    def process_denied_request(request):
        # log the denied request to a file or database
        with open('denied_requests.log', 'a') as f:
            f.write(request.url + '\n')
            

    @flask_app.before_request
    def before_request_func():
        global active_requests
        current_app.start_time = time.perf_counter()
        if active_requests >= max_concurrent_requests:
            process_denied_request.delay(request)
            return "", 202 # accepted but not processed
            # return "Too many requests", 503
        active_requests +=1
        print("New request recieved. Active requests: ", active_requests)

    @flask_app.after_request
    def after_request_func(response):
        global active_requests
        total_time = time.perf_counter() - current_app.start_time
        time_in_ms = int(total_time * 1000)
        current_app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
        active_requests -=1
        print("Request completed. Remaining active requests: ", active_requests)
        return response


    app = FlaskAppWrapper(flask_app)
    app.add_endpoint('/', 'hello_world', app.hello_world)
    app.app.run(debug=True)


#====================================================================================================

