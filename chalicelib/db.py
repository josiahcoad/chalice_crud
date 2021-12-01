from decimal import Decimal

from boto3.dynamodb.conditions import Key


DEFAULT_USERNAME = 'default'


class TodoDB(object):
    def list_items(self):
        pass

    def add_item(self, data, placeid, metadata=None):
        pass

    def get_item(self, placeid):
        pass

    def delete_item(self, placeid):
        pass

    def update_item(self, placeid, description=None, state=None,
                    metadata=None):
        pass


class InMemoryTodoDB(TodoDB):
    def __init__(self, state=None):
        if state is None:
            state = {}
        self._state = state

    def list_all_items(self):
        all_items = []
        for username in self._state:
            all_items.extend(self.list_items(username))
        return all_items

    def list_items(self, username=DEFAULT_USERNAME):
        return self._state.get(username, {})

    def add_item(self, place, placeid, username=DEFAULT_USERNAME):
        if username not in self._state:
            self._state[username] = {}
        self._state[username][placeid] = {
            'place': place,
            'placeid': placeid,
            'username': username
        }
        return placeid

    def get_item(self, placeid, username=DEFAULT_USERNAME):
        return self._state[username][placeid]

    def delete_item(self, placeid, username=DEFAULT_USERNAME):
        del self._state[username][placeid]

    def update_item(self, placeid, description=None, state=None,
                    metadata=None, username=DEFAULT_USERNAME):
        item = self._state[username][placeid]
        if description is not None:
            item['description'] = description
        if state is not None:
            item['state'] = state
        if metadata is not None:
            item['metadata'] = metadata


def replace_floats(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_floats(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = replace_floats(obj[k])
        return obj
    elif isinstance(obj, float):
        return Decimal(str(obj))
    else:
        return obj


class DynamoDBTodo(TodoDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self):
        response = self._table.scan()
        return response['Items']

    def list_items(self, username=DEFAULT_USERNAME):
        response = self._table.query(
            KeyConditionExpression=Key('username').eq(username)
        )
        return response['Items']

    def add_item(self, data, placeid, username=DEFAULT_USERNAME):
        self._table.put_item(
            Item={
                'username': username,
                'placeid': placeid,
                'place': replace_floats(data),
            }
        )
        return placeid

    def get_item(self, placeid, username=DEFAULT_USERNAME):
        response = self._table.get_item(
            Key={
                'username': username,
                'placeid': placeid,
            },
        )
        return response['Item']

    def delete_item(self, placeid, username=DEFAULT_USERNAME):
        self._table.delete_item(
            Key={
                'username': username,
                'placeid': placeid,
            }
        )

    def update_item(self, place, placeid, username=DEFAULT_USERNAME):
        # We could also use update_item() with an UpdateExpression.
        item = self.get_item(placeid, username)
        item['place'] = replace_floats(place)
        self._table.put_item(Item=item)
