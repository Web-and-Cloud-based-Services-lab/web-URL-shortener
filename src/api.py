# This file defines APIs the server provides
# Flask library is used to route APIs
# The use of flask references the official documentation of flask:
# https://flask.palletsprojects.com/en/2.2.x/quickstart/

from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from apiHandler import apiHandler

ERROR_INVALID_REQUEST = "Error: Invalid request"
ERROR_ID_NOT_FOUND = "Error: URL id NOT FOUND"
ERROR_URL_EXISTS = "Error: URL already exists"
ERROR_URL_INVALID = "Error: Invalid URL"
SUCCESS_RETRIEVE = "URL successfully retrieved"
SUCCESS_CREATE = "URL successfully created"
SUCCESS_DELETE = "URL successfully deleted"
SUCCESS_UPDATE = "URL successfully updated"

app = Flask(__name__)
cors = CORS(app) # cors is added in advance to allow cors requests
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=["GET"])
@cross_origin()
def get_keys():
    keys = apiHandler.get_keys()
    return keys

# deletion without an id is not allowed
@app.route('/', methods=["DELETE"])
@cross_origin()
def delete_index():
    return {"message":ERROR_INVALID_REQUEST}, 404

@app.route('/<string:url_id>', methods=["GET"])
@cross_origin()
def get_url(url_id):
    url = apiHandler.get_url(url_id)
    if url == None: # if url == None, then the id used to query does not exist
        return {"message": ERROR_ID_NOT_FOUND}, 404
    return {"message":SUCCESS_RETRIEVE, "data":{"url": url}}, 301

# A url can be added to the database only if:
# 1. the url is valid
# 2. the url does not exist in the database already
@app.route('/', methods=["POST"])
@cross_origin()
def post_url():
    if request.method == 'POST':
        get_data=request.args # get_data gets the body of post request
        get_dict = get_data.to_dict()
        url = get_dict['url']
        if(apiHandler.verify_url(url)): # check if url is valid
            duplicates = apiHandler.detect_duplicates(url)
            if(duplicates['exists']): # check if url already exist
                short_id = duplicates['short_id']
                return {"message": ERROR_URL_EXISTS, "data":{"short_id": short_id} }, 400
            short_id = apiHandler.create_url(url) # add url to database and get the id 
            return {"message": SUCCESS_CREATE, "data": {"short_id": short_id}}, 201
        else:
            return {"message": ERROR_URL_INVALID}, 400

@app.route('/<string:url_id>', methods=["DELETE"])
@cross_origin()
def delete_url(url_id):
    url = apiHandler.get_url(url_id)
    if url == None:
        return {"message": ERROR_ID_NOT_FOUND}, 404
    else:
        apiHandler.delete_url(url_id)
        return {"message": SUCCESS_DELETE}, 204

@app.route('/<string:url_id>', methods=["PUT"])
@cross_origin()
# existence of id and the validity of url are checked first
def update_url(url_id):
    url = apiHandler.get_url(url_id)
    if url == None:
        return {"message": ERROR_ID_NOT_FOUND}, 404
    
    get_data=request.args
    get_dict = get_data.to_dict()
    url = get_dict['url']

    if apiHandler.verify_url(url):
        duplicates = apiHandler.detect_duplicates(url)
        if(duplicates['exists']):
            identity = duplicates['short_id']
            return {"message": ERROR_URL_EXISTS, "data": {"short_id": identity} }, 400
        origin_url = apiHandler.edit_url(url_id, url)
        return {"message": SUCCESS_UPDATE, "data": {"old_url": origin_url, "new_url": url}}, 200
    else:
        return {"message": ERROR_URL_INVALID}, 400
        