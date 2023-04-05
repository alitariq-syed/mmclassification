from flask import Flask, current_app
from gevent.pywsgi import WSGIServer
import logging

app = Flask(__name__)

@app.route('/')
def hello():
    print("print test")
    current_app.logger.setLevel(logging.DEBUG)
    current_app.logger.info("logger info test")
    return 'Hello, World!'

if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()

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