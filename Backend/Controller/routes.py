import tempfile
from random import random, randint

from flask import request, json
from werkzeug.utils import secure_filename

from .app import app
from .dataformats import SearchResponse
from .parser import parse


@app.route('/upload', methods=['post'])
def uploadFile():
    if 'seqfile' not in request.files:
        return json.jsonify({'error': 'No file specified'})

    resp = SearchResponse()
    for i in range(0, 10):
        vendor_id = randint(0, 1)
        resp.result[0]['offers'].append({
            "vendorinformation": {
                "name": "Twist DNA ..." if vendor_id == 0 else "IDT DNA ...",
                "shortname": "Twist" if vendor_id == 0 else "IDT",
                "key": ""
            },
            "price": random(),
            "turnovertime": randint(1, 20)
        })

    #
    #   TODO: Arr, Here be stuff for populating the response object such as file parsing!
    #
    tempf = tempfile.mkstemp('.' + secure_filename(request.files['seqfile'].filename).rsplit('.', 1)[1].lower())
    request.files['seqfile'].save(tempf)
    parse(tempf)

    return json.jsonify(resp.__dict__)
