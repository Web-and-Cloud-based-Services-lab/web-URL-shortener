from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from apiHandler import apiHandler


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def index():
    return "Server Connected"

@app.route('/', methods=["POST"])
def post_url():
    if request.method == 'POST':
        get_data=request.args
        get_dict = get_data.to_dict()
        url = get_dict['url']
        if(apiHandler.verify_url(url)):
            response = apiHandler.create_url(url)
            return response, 201
        else:
            return "Invalid URL", 400

@app.route('/<string:url_id>', methods=["GET"])
def get_url(url_id):
    return "get : "+ url_id, 301
