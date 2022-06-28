import json
import boto3
from datetime import date, datetime
import requests
import pandas as pd

from io import StringIO 

def lambda_handler(event=None, context=None):

    #num_serie = 20573
    num_serie = event['serie']

    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{num_serie}/dados?formato=json'
    resp = requests.get(url=url)

    if resp.status_code == 200 and resp.headers['content-type'] == 'application/json; charset=utf-8':
        df_data = pd.DataFrame(resp.json())
        df_data['serie'] = str(num_serie)

        csv_buffer = StringIO()
        df_data.to_csv(csv_buffer, index=False)
        timestamp = datetime.now().strftime("%m%Y")

        s3_client = boto3.client('s3', region_name='us-east-2')
        s3_client.put_object(Body=csv_buffer.getvalue(), Bucket='s3-zone-raw', Key=f'_partitiontime={timestamp}/{num_serie}.csv')

        return {
            "message": "Success",
            "s3_uri": f"s3://s3-zone-raw/_partitiontime={timestamp}/"
        }


if __name__ == '__main__':
    lambda_handler()
    
    # num_serie = event['serie']
    
    # url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{num_serie}/dados?formato=json'

    #return 
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps(event)
    # }

