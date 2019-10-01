from chalice import Chalice
from chalice import BadRequestError

app = Chalice(app_name='helloworld')
app.debug = True

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
