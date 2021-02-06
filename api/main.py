from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from io import BytesIO
from separater import Separater
from youtube.main import YouTube
import os
from waitress import serve


app = Flask(__name__, static_folder=None)
CORS(app)

separater = Separater()

status = separater.load_model(
    path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models/model.th')
)

@app.route('/', methods=['GET'])
def help():

    response = make_response(
        'usage: curl -X POST {} -F @path/to/audio/file.wav -o path/to/output.zip'.format(os.environ['HOST']),
        200
    )
    response.mimetype = "text/plain"
    return response



@app.route('/separate', methods=['POST'])
def separate():

    if separater.model is None:
        return jsonify({"status": "error", "code": 500, "message": "some error occured."})

    request_audio_buffer = BytesIO(request.files["file"].stream.read())
    source_zip_buffer = separater(buffer=request_audio_buffer)

    res = make_response(source_zip_buffer.getvalue())
    source_zip_buffer.close()

    res.headers['Content-Type'] = 'application/zip'
    res.headers['Content-Disposition'] = 'attachment; filename=sounds.zip'
    return res


@app.route('/separate/<id>', methods=['GET'])
def separate_yt(id):

    if separater.model is None:
        return jsonify({"status": "error", "code": 500, "message": "some error occured."})

    path = YouTube()(id)
    source_zip_buffer = separater(path=path)
    os.remove(path)

    res = make_response(source_zip_buffer.getvalue())
    source_zip_buffer.close()

    res.headers['Content-Type'] = 'application/zip'
    res.headers['Content-Disposition'] = 'attachment; filename=sounds.zip'
    return res


if __name__ == "__main__":
    if os.environ['py_env'] == "production":
        serve(app, host='0.0.0.0', port=os.environ['PORT'])
    else:
        app.run(debug=True, port=os.environ['PORT'])
