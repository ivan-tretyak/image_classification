from flask import Flask, request, json
from algorithm.main import string_to_PIL, main, get_clss, load_model

app = Flask(__name__)

#model = load_model()
clss = get_clss()

@app.route('/', methods=["POST"])
def hello_world():  # put application's code here
    data = request.data
    data = json.loads(data)
    #image = string_to_PIL(data['image'])
    #cls = main(model, clss, image)
    return json.dumps(data)

if __name__ == '__main__':
    app.run()