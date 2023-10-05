import boto3


def create_music_table(dynamodb=None):

    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')  # ,
        # endpoint_url="http://localhost:8000")
        table = dynamodb.create_table(
            TableName='subscription',
            KeySchema=[
                {
                    'AttributeName': 'title',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                },
                # {
                #     'AttributeName': 'artist',
                #     'AttributeType': 'S'
                # },
                # {
                #     'AttributeName': 'year',
                #     'AttributeType': 'N'
                # },
                # {
                #     'AttributeName': 'web_url',
                #     'AttributeType': 'S'
                # },
                # {
                #     'AttributeName': 'image_url',
                #     'AttributeType': 'S'
                # }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    return table


if __name__ == '__main__':
    movie_table = create_music_table()
    print("Table status:", movie_table.table_status)
