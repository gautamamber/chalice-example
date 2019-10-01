from chalice import Chalice, Response, CORSConfig
from chalice import BadRequestError, NotFoundError
import boto3
import uuid

dynamo = boto3.resource("dynamodb")

app = Chalice(app_name='helloworld')
app.debug = True

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['X-Special-Header'],
    max_age=600,
    expose_headers=['X-Special-Header'],
    allow_credentials=True
)
table = dynamo.Table("usertable")
OBJECTS = {}
@app.route('/')
def index():
    return {'hello': 'world'}

# url parameters

CITIES_OF_STATE = {
    "seattle": "WA",
    "portland": "OR"
}

@app.route('/cities/{city}')
def state_of_city(city):
    try:
        return {"state": CITIES_OF_STATE[city]}
    except KeyError:
        raise BadRequestError("Unknown city '%s', valid choices are: %s" % (city, ','.join(CITIES_OF_STATE.keys())))

# url put or post methods
@app.route('/resource/{value}', methods=['PUT', 'POST'])
def put_test(value):
    data = {
        "value" : value
    }
    return data

# Request meta data
@app.route('/objects/{key}', methods = ['GET', 'PUT'])
def myobject(key):
    request = app.current_request
    print(request.json_body)
    if request.method == 'PUT':
        OBJECTS[key] = request.json_body
    elif request.method == 'GET':
        try:
            return {key: OBJECTS[key]}
        except KeyError:
            raise NotFoundError(key)
    
@app.route('/custom-response')
def custom_response():
    return Response(
        body = "Hello world",
        status_code = 200,
        headers = {"Content-Type" : "text/plain"}
    )

@app.route('/custom-cors', methods = ['GET'], cors = cors_config)
def support_cors():
    return {
        "cors": True
    }

# Add data to dynamoDB
@app.route('/add-user', methods = ['POST'], cors = cors_config)
def add_user():
    table.put_item(
        Item = {
            "username": str(uuid.uuid4()),
            "name": "Mark Lyn",
            "age": 23,
            "city": "NYC"
        }
    )
    data = {
        "result": "Success"
    }
    return data

# Get item from dyanamo

@app.route('/get-user/{username}', methods = ['GET'])
def get_user(username):
    request = app.current_request
    if request.method == "GET":
        data = table.get_item(
            Key = {
                "username": username
            }
        )
    return {
        "result" : data
    }