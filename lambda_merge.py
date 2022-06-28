from datetime import datetime
import pandas as pd
import boto3
import glob
import os

def clear_folder():
    try:
        files = glob.glob('/tmp/*')
        for f in files:
            os.remove(f)
    except:
        ...

def lambda_handler(event=None, context=None):

    envelop = event['s3_uri'].split("/")
    s3_partition = envelop[3]
    s3_name = envelop[2]

    clear_folder()

    s3_client = boto3.client('s3', region_name='us-east-2')
    for item in s3_client.list_objects(Bucket=s3_name, Prefix= s3_partition)['Contents']:
        item_name = item['Key'].split('/')[1]
        s3_client.download_file(s3_name, item['Key'], f'/tmp/{item_name}')

    files = os.path.join("/tmp/", "*.csv")
    files = glob.glob(files)
    merged_df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    merged_df.to_csv("/tmp/data.csv", index=False)

    s3_client.upload_file("/tmp/data.csv", "s3-zone-trusted", f'{s3_partition}/data.csv')

    clear_folder()

    return {
        "message": "Success",
        "s3_uri": f"s3://s3-zone-trusted/{s3_partition}/data.csv"
    }


if __name__ == '__main__':
    teste = {"s3_uri": "s3://s3-zone-raw/_partitiontime=062022/"}
    lambda_handler(event=teste)
    
    # num_serie = event['serie']
    
    # url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{num_serie}/dados?formato=json'



