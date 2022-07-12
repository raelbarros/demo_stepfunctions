import json
import boto3
from datetime import datetime

def lambda_handler():

    s3_client = boto3.client('s3', 
        aws_access_key_id=,
        aws_secret_access_key=,
        region_name='us-east-2'
    )

    s3_client.download_file('s3-configs-lambda', 'series-temporais/config.json', 'config.json')
    with open('config.json') as config_file:
        config = json.loads(config_file.read())

    list_item = []
    for item in  config['LIST_SERIES']:
        list_item.append({"serie": item})

    response = {}
    response["list_series"] = list_item

    print(response)


if __name__ == '__main__':
    lambda_handler()
    
