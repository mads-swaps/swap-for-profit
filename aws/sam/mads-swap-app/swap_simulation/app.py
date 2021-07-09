import json
import urllib3
import boto3
import os
import psycopg2
import pandas as pd
import buy_decision
import price_decision

http = urllib3.PoolManager()

client = boto3.client('ssm')
pghost = os.environ['PGHOST']
pgport = 5432
pgdb = os.environ['PGDBNAME']
pguser = os.environ['PGUSER']
pgpass = os.environ['PGPASSLOCAL']
if pgpass == "":
    parameter = client.get_parameter(Name='binance-crawler-password', WithDecryption=True)
    pgpass = parameter['Parameter']['Value']

conn = psycopg2.connect(host=pghost, database=pgdb, user=pguser, password=pgpass, connect_timeout=3)

def get_latest_candlestick(symbol='ETHBTC'):
    sql = f"""
select * from candlestick_15m cm 
inner join pairs p on cm.pair_id = p.id 
where p.symbol = '{symbol}' and cm.close_time notnull 
order by cm.open_time desc limit 1
"""
    df = pd.read_sql_query(sql, conn)
    return df


def lambda_handler(event, context):
    data = get_latest_candlestick()
    return {
        'statusCode': 200,
        'body': json.dumps({"data":len(data)})
    }