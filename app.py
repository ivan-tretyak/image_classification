from flask import Flask, request, views

from algorithm.main import main, load_model
from jsonapi.utils import *
from jsonapi.validate import validate_json

app = Flask(__name__)
model = load_model()


class ImageClassifier(views.MethodView):
    content_type = {'Content-Type': 'application/vnd.api+json'}

    def post(self):
        if request.headers['Content-Type'] == 'application/vnd.api+json' and request.headers['Accept'] == 'application/vnd.api+json':
            validate_json(request.json)
            cls_number, clss = main(model, request.json)
            data = {'data':
                        {
                            'type':'object_on_photo',
                            'id':cls_number,
                             'attributes':
                                 {
                                     'text':clss
                                 },
                             'language':'en'
                        }
                    }
            return create_response(200, data)
        elif request.headers['Content-Type'] == 'application/vnd.api+json' and request.mimetype_params != {}:
            return create_error_response(415, 'Mimetype parametres is not empty.')
        elif request.headers['Content-Type'] == 'application/vnd.api+json' and request.headers['Accept'] != 'application/vnd.api+json':
            create_error_response(415, 'Header \'Accept\' is not \'application/vnd.api+json\'')


def main():
    app.add_url_rule('/classification', view_func=ImageClassifier.as_view('classification'))
    app.register_error_handler(404, resource_not_exists)
    app.register_error_handler(500, server_error)
    app.register_error_handler(405, method_is_not_allowed)
    app.register_error_handler(400, handle_invalid_usage)
    app.register_error_handler(Exception, server_error)
    app.run()

if __name__ == '__main__':
    main()