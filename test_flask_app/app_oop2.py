from flask import Flask, current_app, request
import time

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

class FlaskAppWrapper(object):

    def __init__(self, app, **configs):
        self.app = app

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)
    
    def hello_world(self):
        return "Hello, world!"
    
    def run(self, **kwargs):
        self.app.run(**kwargs)

if __name__ == "__main__":

    flask_app = Flask(__name__)

    @flask_app.before_request
    def before_request_func():
        current_app.start_time = time.perf_counter()

    @flask_app.after_request
    def after_request_func(response):
        total_time = time.perf_counter() - current_app.start_time
        time_in_ms = int(total_time * 1000)
        current_app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
        return response


    app = FlaskAppWrapper(flask_app)
    app.add_endpoint('/', 'hello_world', app.hello_world)
    app.app.run(debug=True)


#====================================================================================================

