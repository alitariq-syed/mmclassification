
import time
from flask import Flask, request, jsonify, current_app, g

# class FlaskAppWrapper(object):
#     # super().__init__(*args, **kwargs)

#     def __init__(self, app, **configs):
#         self.app = app
#         self.configs(**configs)
#         # Add before request function
#         self.before_request(self.before_request_func)
#         self.after_request(self.after_request_func)

#     # def configs(self, **configs):
#     #     for config, value in configs:
#     #         self.app.config[config.upper()] = value

#     def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
#         self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

#     def before_request_func(self):
#         current_app.start_time = time.perf_counter()

#     def after_request_func(self, response):
#         total_time = time.perf_counter() - current_app.start_time
#         time_in_ms = int(total_time * 1000)
#         # Log the time taken for the endpoint 
#         current_app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
#         return response
        
#     def run(self, **kwargs):
#         self.app.run(**kwargs)


# flask_app = Flask(__name__)

# app = FlaskAppWrapper(flask_app)

#====================================================================================================


from flask import Flask, current_app, jsonify, request
import time

class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add before and after request functions
        self.before_request(self.before_request_func)
        self.after_request(self.after_request_func)

        # Define routes
        self.add_url_rule('/', 'index', self.index)

    def before_request_func(self):
        # g.user = get_current_user()  # Replace with your own authentication function
        # print("starting time before request")
        print("current_app.classification_model before request",current_app.classification_model)
        current_app.start_time = time.perf_counter()


    def after_request_func(self, response):
        # print("ending time after request")
        # Get total time in milliseconds
        total_time = time.perf_counter() - current_app.start_time
        time_in_ms = int(total_time * 1000)
        # Log the time taken for the endpoint 
        current_app.logger.info('%s %s ms %s %s %s', "Total request response time: ", time_in_ms, request.method, request.path, dict(request.args))
        return response

    def index(self):
        time.sleep(2)
        return jsonify({'message': f'Hello, world!'})

if __name__ == '__main__':
    app = MyApp(__name__)
    with app.app_context():
        current_app.classification_model = "my classification model"
        current_app.segmentation_model = "my segmentation model"
    app.run(debug = True)
