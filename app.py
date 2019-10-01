from chalice import Chalice
from chalice import BadRequestError, NotFoundError

app = Chalice(app_name='helloworld')
app.debug = True
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
