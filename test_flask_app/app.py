
import time
from flask import Flask, request, jsonify, current_app, g

app = Flask(__name__)
print("loading models.....")

@app.before_request
def logging_before():
    # Store the start time for the request
    current_app.start_time = time.perf_counter()


@app.after_request
def logging_after(response):
    # Get total time in milliseconds
    total_time = time.perf_counter() - current_app.start_time
    time_in_ms = int(total_time * 1000)
    # Log the time taken for the endpoint 
    current_app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    return response


@app.get('/')
def home():
    # artificial delay
    time.sleep(1.3)
    print(current_app.classification_model)
    return jsonify({'Hello': 'World!!'})


@app.get('/slow-request')
def slow_request():
    # artificial delay
    time.sleep(5)
    print(current_app.segmentation_model)

    return jsonify({'msg': 'slow request'})


if __name__ == '__main__':
    with app.app_context():
        current_app.classification_model = "my classification model"
        current_app.segmentation_model = "my segmentation model"
    app.run(debug=True)
