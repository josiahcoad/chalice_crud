from decimal import Decimal
from uuid import uuid4


class DB:
    def list_items(self):
        pass

    def add_item(self, data):
        pass

    def get_item(self, id):
        pass

    def delete_item(self, id):
        pass

    def update_item(self, data, id):
        pass


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


class DynamoDB(DB):
    def __init__(self, table_resource):
        self._table = table_resource

    def list_all_items(self):
        response = self._table.scan()
        return response['Items']

    def add_item(self, data):
        id = str(uuid4())
        self._table.put_item(
            Item={
                'id': id,
                'data': replace_floats(data),
            }
        )
        return id

    def get_item(self, id):
        response = self._table.get_item(
            Key={
                'id': id,
            },
        )
        return response['Item']

    def delete_item(self, id):
        self._table.delete_item(
            Key={
                'id': id,
            }
        )

    def update_item(self, data, id):
        item = self.get_item(id)
        item['data'] = replace_floats(data)
        self._table.put_item(Item=item)
