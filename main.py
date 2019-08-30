import json
import uuid

from boto3 import resource
from boto3.dynamodb.conditions import Key
import os

# Constants for the AWS API Gateway
HTTP_PROXY_STATUS_CODE_RESPONSE = "statusCode"
HTTP_PROXY_METHOD_NAME = "httpMethod"
HTTP_PROXY_BODY_NAME = "body"

# Cosntants for the Model expected to be received for this function.
MODEL_PAYLOAD = "payload"

# The boto3 dynamoDB resource
dynamodb_resource = resource('dynamodb')

tableName = os.environ['DB_TABLE_NAME']
print("table: %s", tableName)
table = dynamodb_resource.Table(tableName)

return_dict = dict()
return_dict["isBase64Encoded"] = False


def lambda_handler(event, context):
    """
    Main handler for lambda functions
    """
    # print(get_table_metadata())
    ev = event[HTTP_PROXY_BODY_NAME]
    body = json.loads(ev)
    operation = event[HTTP_PROXY_METHOD_NAME]
    if operation == "notfound":
        return_dict[HTTP_PROXY_BODY_NAME] = "{'message': 'Unknown operation.'}"
        return_dict[HTTP_PROXY_STATUS_CODE_RESPONSE] = 400
        return return_dict

    elif (operation == "POST"):
        print("creating Record...")
        response = add_item(body[MODEL_PAYLOAD])
        return_dict[HTTP_PROXY_STATUS_CODE_RESPONSE] = 202
        return_dict[HTTP_PROXY_BODY_NAME] = "Request Successfully Received!"
        return return_dict

    elif (operation == "GET"):
        return scan_table()
    elif (operation == "echo"):
        return "echo successful"


def get_table_metadata():
    """
    Get some metadata about chosen table.
    """
    return {
        'num_items': table.item_count,
        'primary_key_name': table.key_schema[0],
        'status': table.table_status,
        'bytes_size': table.table_size_bytes,
        'global_secondary_indices': table.global_secondary_indexes
    }


def read_table_item(pk_name, pk_value):
    """
    Return item read by primary key.
    """
    response = table.get_item(Key={pk_name: pk_value})

    return response


def add_item(col_dict):
    """
    Add one item (row) to table. col_dict is a dictionary {col_name: value}.
    """
    # ADD ID
    col_dict["id"] = str(uuid.uuid1())
    response = table.put_item(Item=col_dict)

    return response


def delete_item(pk_name, pk_value):
    """
    Delete an item (row) in table from its primary key.
    """
    response = table.delete_item(Key={pk_name: pk_value})

    return response


def scan_table(filter_key=None, filter_value=None):
    """
    Perform a scan operation on table.
    Can specify filter_key (col name) and its value to be filtered.
    """
    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()

    return response


def query_table(filter_key=None, filter_value=None):
    """
    Perform a query operation on the table.
    Can specify filter_key (col name) and its value to be filtered.
    """
    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        response = table.query(KeyConditionExpression=filtering_exp)
    else:
        response = table.query()

    return response