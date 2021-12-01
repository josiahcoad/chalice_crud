from chalice import Chalice
from chalicelib import db
import os
import boto3

app = Chalice(app_name='forthepeople')
app.debug = True
_DB = None


def get_app_db():
    global _DB
    if _DB is None:
        _DB = db.DynamoDB(
            boto3.resource('dynamodb').Table(
                os.environ['APP_TABLE_NAME'])
        )
    return _DB


# CRUD
@app.route('/', methods=['GET'], cors=True)
def test():
    return {'message': 'success'}


@app.route('/items', methods=['GET'], cors=True)
def get_all():
    return get_app_db().list_all_items()


@app.route('/items', methods=['POST'], cors=True)
def create():
    body = app.current_request.json_body
    return get_app_db().add_item(body)


@app.route('/items/{id}', methods=['GET'], cors=True)
def get(id):
    return get_app_db().get_item(id)


@app.route('/items/{id}', methods=['DELETE'], cors=True)
def delete(id):
    return get_app_db().delete_item(id)


@app.route('/items/{id}', methods=['PUT'], cors=True)
def update(id):
    body = app.current_request.json_body
    get_app_db().update_item(body, id)
