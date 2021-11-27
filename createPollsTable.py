import boto3


def create_poll_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='Polls',
        KeySchema=[
            {
                'AttributeName': 'pollID', #notes only takes decimal
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'createdBy',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
             {
                "AttributeName": "pollID",
                "AttributeType": "N"
            },
            {
                "AttributeName": "createdBy",
                "AttributeType": "S"
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


if __name__ == '__main__':
    poll_table = create_poll_table()
    print("Table status:", poll_table.table_status)