import time

from flask import Flask, request, render_template
app = Flask(__name__)
from image import recognize, registrate

registered = {}


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/rec', methods=['POST'])
def recognize_req():
    content_type = request.headers.get('Content-Type')

    if content_type.find('application/json') == -1:
        return 'Content-Type not supported!'

    json_ = request.json
    result = recognize(json_['image'])
    identity = []

    for each in result[0]:
        name = registered.get(each)

        if name is None:
            name = 'Unknown'

        identity.append([each, name])

    return {'rec': identity, 'data': result[1]}


@app.route('/reg', methods=['POST'])
def register_req():
    content_type = request.headers.get('Content-Type')

    if content_type.find('application/json') == -1:
        return 'Content-Type not supported!'

    json_ = request.json

    registrate(json_['id'].upper(), json_['image'])
    registered[json_['id'].upper()] = json_['name'].upper()

    for x in range(10):
        result = recognize(json_['image'])

        if len(result[0]) > 0:
            break

        time.sleep(1)

    identity = []

    for each in result[0]:
        name = registered.get(each)

        if name is None:
            name = 'Unknown'

        identity.append([each, name])

    return {'rec': identity, 'data': result[1]}


if __name__ == "__main__":
    app.run()