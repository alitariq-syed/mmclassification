from flask import Flask, current_app, request
from gevent.pywsgi import WSGIServer
import logging
import time

max_concurrent_requests = 3
active_requests = 0


app = Flask(__name__)

@app.before_request
def before_request_func():
    global active_requests
    current_app.start_time = time.perf_counter()
    # if active_requests >= max_concurrent_requests:
    #     return "Too many requests", 503
    active_requests +=1
    print("New request recieved. Active requests: ", active_requests)

@app.after_request
def after_request_func(response):
    global active_requests
    total_time = time.perf_counter() - current_app.start_time
    time_in_ms = int(total_time * 1000)
    current_app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    active_requests -=1
    print("Request completed. Remaining active requests: ", active_requests)
    return response



@app.route('/')
def hello():
    print("print test")
    time.sleep(5)
    current_app.logger.setLevel(logging.DEBUG)
    current_app.logger.info("logger info test")
    return 'Hello, World!'

# if __name__ == '__main__':
#     # Debug/Development
#     # app.run(debug=True, host="0.0.0.0", port="5000")
#     # Production
#     http_server = WSGIServer(('0.0.0.0', 5000), app)
#     http_server.serve_forever()
if __name__ == '__main__':
    from waitress import serve
    # with app.app_context:
    #     current_app.logger.setLevel(logging.DEBUG)
    serve(app, host='0.0.0.0', port=5000, threads = 4)
################################################################################
################################################################################

# from flask import Flask, current_app
# import logging
# app = Flask(__name__)

# @app.route('/')
# def hello():
#     print("print test")
#     current_app.logger.setLevel(logging.DEBUG)
#     current_app.logger.info("logger info test")
#     return 'Hello, World!'

# if __name__ == '__main__':
#     from waitress import serve
#     # with app.app_context:
#     #     current_app.logger.setLevel(logging.DEBUG)
#     serve(app, host='0.0.0.0', port=8080)