# This file defines APIs the server provides
# Flask library is used to route APIs
# The use of flask references the official documentation of flask:
# https://flask.palletsprojects.com/en/2.2.x/quickstart/

from flask import Flask, request, g
from flask_cors import CORS, cross_origin
from apiHandler import apiHandler

ERROR_INVALID_REQUEST = "Error: Invalid request"
ERROR_ID_NOT_FOUND = "Error: URL id NOT FOUND"
ERROR_URL_EXISTS = "Error: URL already exists"
ERROR_URL_INVALID = "Error: Invalid URL"
ERROR_FORBIDDEN = "Error: Forbidden"
SUCCESS_RETRIEVE = "URL successfully retrieved"
SUCCESS_CREATE = "URL successfully created"
SUCCESS_DELETE = "URL successfully deleted"
SUCCESS_UPDATE = "URL successfully updated"

app = Flask(__name__)
cors = CORS(app) # cors is added in advance to allow cors requests
app.config['CORS_HEADERS'] = 'Content-Type'

ENDPOINT_WITHOUT_AUTH = ['delete_index', 'get_url']

# @cross_origin() can not be added infront of endpoints anymore, 
# otherwise the endpoints will not be called after before_request 

@app.before_request
def verify_user():
    if request.endpoint in ENDPOINT_WITHOUT_AUTH:
        return None
    jwt = request.args.to_dict()['jwt']
    auth_res = apiHandler.verify_user(jwt)
    if not auth_res['valid'] or auth_res['username'] is None:
        return {"message":ERROR_FORBIDDEN}, 403
    g.username = auth_res['username']

@app.after_request
def after_request(response):
    # to enable cors response
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/', methods=["GET"])
def get_keys():
    keys = apiHandler.get_keys(g.username)
    return keys, 200

# deletion without an id is not allowed
@app.route('/', methods=["DELETE"])
def delete_index():
    return {"message":ERROR_INVALID_REQUEST}, 404

@app.route('/<string:url_id>', methods=["GET"])
def get_url(url_id):
    record = apiHandler.get_url(url_id)
    if record == None: # if url == None, then the id used to query does not exist
        return {"message": ERROR_ID_NOT_FOUND}, 404
    return {"message":SUCCESS_RETRIEVE, "data":{"url": record['url']}}, 301

# A url can be added to the database only if:
# 1. the url is valid
# 2. the url does not exist in the database already
@app.route('/', methods=["POST"])
def post_url():
    if request.method == 'POST':
        url = request.args.to_dict()['url']

        if(apiHandler.verify_url(url)): # check if url is valid
            duplicates = apiHandler.detect_duplicates(url)
            if(duplicates['exists']): # check if url already exist
                return {"message": ERROR_URL_EXISTS, "data":{"short_id": duplicates['short_id']} }, 400
            short_id = apiHandler.create_url(url, g.username) # add url to database and get the id 
            return {"message": SUCCESS_CREATE, "data": {"short_id": short_id, "url": url}}, 201
        else:
            return {"message": ERROR_URL_INVALID}, 400

@app.route('/<string:url_id>', methods=["DELETE"])
def delete_url(url_id):
    record = apiHandler.get_url(url_id)
    if record == None:
        return {"message": ERROR_ID_NOT_FOUND}, 404
    if record['username'] is None or record['username'] != g.username:
        return {"message":ERROR_FORBIDDEN}, 403
    apiHandler.delete_url(url_id)
    return {"message": SUCCESS_DELETE}, 204

@app.route('/<string:url_id>', methods=["PUT"])
# existence of id and the validity of url are checked first
def update_url(url_id):
    record = apiHandler.get_url(url_id)
    if record == None:
        return {"message": ERROR_ID_NOT_FOUND}, 404
    if record['username'] is None or record['username'] != g.username:
        return {"message":ERROR_FORBIDDEN}, 403

    new_url=request.args.to_dict()['url']

    if apiHandler.verify_url(new_url):
        duplicates = apiHandler.detect_duplicates(new_url)
        if(duplicates['exists']):
            return {"message": ERROR_URL_EXISTS, "data": {"short_id": duplicates['short_id']} }, 400
        apiHandler.edit_url(url_id, new_url)
        return {"message": SUCCESS_UPDATE, "data": {"short_id":url_id, "old_url": record['url'], "new_url": new_url}}, 200
    else:
        return {"message": ERROR_URL_INVALID}, 400


