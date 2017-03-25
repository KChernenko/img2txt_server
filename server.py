from flask import Flask, request, make_response, abort
from img2txt import process_image

app = Flask(__name__)


@app.route('/process_image', methods=['POST'])
def hello():

    try:
        image = request.files['upload'].stream
        size = int(request.args.get('size', 50))
        ratio = float(request.args.get('ratio', 1.0))
        antialias = int(request.args.get('antialias', 0)) == 1
    except (ValueError, KeyError):
        abort(400)

    result_image = process_image(image, antialias, size, ratio)
    return make_response(result_image)


if __name__ == "__main__":
    app.run(port=8088)
