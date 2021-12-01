from chalice import Chalice
from chalicelib import db, logic, gmaps
import os
import boto3

app = Chalice(app_name='mytodo')
app.debug = True
_DB = None


def get_app_db():
    global _DB
    if _DB is None:
        _DB = db.DynamoDBTodo(
            boto3.resource('dynamodb').Table(
                os.environ['APP_TABLE_NAME'])
        )
    return _DB


# CRUD
@app.route('/', methods=['GET'], cors=True)
def test():
    return {'message': 'success'}


@app.route('/places', methods=['GET'], cors=True)
def get_all():
    return get_app_db().list_all_items()


@app.route('/places', methods=['POST'], cors=True)
def create():
    body = app.current_request.json_body
    return get_app_db().add_item(body['place'], body['placeid'])


@app.route('/places/{placeid}', methods=['GET'], cors=True)
def get(placeid):
    return get_app_db().get_item(placeid)


@app.route('/places/{placeid}', methods=['DELETE'], cors=True)
def delete(placeid):
    return get_app_db().delete_item(placeid)


@app.route('/places/{placeid}', methods=['PUT'], cors=True)
def update(placeid):
    body = app.current_request.json_body
    get_app_db().update_item(body['place'], placeid)


# higher level logic
@app.route('/places/now/{datetime}', methods=['GET'], cors=True)
def get_happening_now(datetime):
    day, time = datetime.split('%20')  # url encoding for space
    # day in ['Monday', 'Tuesday', ...]
    # time formatted like: '3:00P'
    data = get_all()
    places = {item['placeid']: item['place'] for item in data}
    happening = logic.happening_now(day, time, places)
    return [gmaps.merge_place_details(place_id, place) for place_id, place in happening.items()]
