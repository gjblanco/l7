from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import os
import io

from .db import initdb, drop_all, save_file_piece, read_file_linebyline
from .datahandle import count_by_leading_digit

app = Flask(__name__)
initdb(app)

@app.route('/uploaddata', methods=["POST"])
def uploaddata():
    if request.method == "POST":
        reqjson = request.get_json()
        filename = request.json.get('filename', None)
        file_id = request.json.get('fileId', None)
        contents = request.json.get('contents', None)
        is_last_chunk = request.json.get('isLastChunk', False)
        
        if contents is None:
            return "contents cannot be empty", 400

        print("islastchunk", is_last_chunk)
        result = save_file_piece(filename, contents, None, is_last_chunk, file_id)
#        save_file(file)
#        for delimiter in DELIMITERS:
#            stream.seek(0)
#            ans = count_by_leading_digit(io.StringIO(stream.read().decode("UTF8"), newline=None), delimiter)
#            if ans != None:
#                break
        return jsonify(fileId=result[0][0])

@app.route('/processdata/<int:fileid>', methods=["GET"])
def processdata(fileid):
    print("THEPARAM", fileid)
    
    DELIMITERS = [',', '\t', '|']
    for delimiter in DELIMITERS:
        stream = read_file_linebyline(fileid)
        for s in stream:
            print('SS', s)
        ans = count_by_leading_digit(read_file_linebyline(fileid), delimiter)
        if ans != None:
            break
    return jsonify(ans)


@app.route("/")
def hello_world():
    return jsonify(hello="world")
