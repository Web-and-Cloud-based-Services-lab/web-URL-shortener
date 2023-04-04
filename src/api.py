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
def post_outlet():
    if request.method == 'POST':
        get_data=request.args
        apiHandler.create_url(get_data.to_dict())
        

    return 'insert successfully'
