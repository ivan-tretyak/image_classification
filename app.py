from flask import Flask, request

import jsonapi.validate
from algorithm.main import main, load_model
from jsonapi.utils import *
from jsonapi.validate import validate_json

app = Flask(__name__)
print('Model load')
model = load_model()
print('Model loaded')


@app.route('/', methods=["POST"])
def post():
    print(request.headers)
    if request.headers['Content-Type'] == 'application/vnd.api+json' and request.headers.get('Accept', None) == 'application/vnd.api+json':
        validate_json(request.json)
        cls_number, clss = main(model, request.json)
        data = {'data':
            {
                'type': 'object_on_photo',
                'id': cls_number,
                'attributes':
                    {
                        'text': clss
                    },
                'language': 'en'
            }
        }
        return create_response(200, data)
    elif request.headers['Content-Type'] == 'application/vnd.api+json' and request.mimetype_params != {}:
        return create_error_response(415, 'Mimetype parametres is not empty.')
    elif request.headers['Content-Type'] == 'application/vnd.api+json' and request.headers.get('Accept', None) != 'application/vnd.api+json':
        return create_error_response(415, 'Header \'Accept\' is not \'application/vnd.api+json\'')
    else:
        return create_error_response(415, "Unknown access error")


app.register_error_handler(404, resource_not_exists)
app.register_error_handler(500, server_error)
app.register_error_handler(405, method_is_not_allowed)
app.register_error_handler(400, handle_invalid_usage)
app.register_error_handler(jsonapi.validate.InvalidApiUsage, handle_invalid_usage)

if __name__ == '__main__':
    app.run()
