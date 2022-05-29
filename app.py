from flask import Flask, request, jsonify, abort
from algorithm.main import main, load_model


app = Flask(__name__)
print('Model load')
model = load_model()
print('Model loaded')


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal server error"})


@app.route('/', methods=["POST"])
def post():
    try:
        cls = main(model, request.json)
        data = {'data': {'type': 'object on photo', 'class_name':cls[1], 'class_number':cls[0]}}
        return jsonify(data)
    except:
        abort(500)

if __name__ == '__main__':
    app.run()
