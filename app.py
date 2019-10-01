from chalice import Chalice

app = Chalice(app_name='helloworld')


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
    data = {
        "state": CITIES_OF_STATE[city]
    }
    return data
