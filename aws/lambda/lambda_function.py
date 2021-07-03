import json
import urllib3
import boto3
import os
import psycopg2

http = urllib3.PoolManager()

client = boto3.client('ssm')
parameter = client.get_parameter(Name='[REDACTED]', WithDecryption=True)
pghost = '[REDACTED]'
pgport = 999999999
pgdb = '[REDACTED]'
pguser = '[REDACTED]'
pgpass = parameter['Parameter']['Value']

conn = psycopg2.connect(host=pghost, database=pgdb, user=pguser, password=pgpass, connect_timeout=3)

def get_latest_epoch():
    sql = """
select
    d.pair_id as id,
    p.symbol,
    d.start_epoch
from
    (
        select
            pair_id, extract(epoch from max(open_time))::numeric::integer as start_epoch
        from candlestick_15m
        group by pair_id
    ) d
inner join
    pairs p on p.id = d.pair_id
"""
    cur = conn.cursor()
    cur.execute(sql)
    r = cur.fetchall()
    cur.close()
    return r

def crawl_data(symbol,epoch):
    resp = http.request("GET", f"https://www.binance.com/api/v1/klines?symbol={symbol}&interval=15m&limit=1000&startTime={epoch}000")
    if resp.status==200:
        return json.loads(resp.data.replace(b'"',b''))
    else:
        return []
        
def insert_data(records):
    sql_values = []
    for pid,rows in records.items():
        for i,r in enumerate(rows[::-1]):
            fields = [str(pid)] + [str(f) for f in r][:-1]
            fields[1] = f"to_timestamp({fields[1][:-3]})"
            fields[7] = f"to_timestamp({fields[7][:-3]})"
            if i == 0:
                fields[7] = "NULL"
            sql_values.append("(" + (",".join(fields)) + ")")
    if len(sql_values) == 0:
        return "",-1
    query_values = ",\n    ".join(sql_values)
    sql = f"""
insert into candlestick_15m (pair_id, open_time, "open", high, low, "close", volume,  close_time,
    quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume)
values
    {query_values}
on conflict (pair_id, open_time)
    do update
set
    "open" = excluded."open",
    high = excluded.high,
    low = excluded.low,
    "close" = excluded."close",
    volume = excluded.volume,
    close_time = excluded.close_time,
    quote_asset_volume = excluded.quote_asset_volume,
    number_of_trades = excluded.number_of_trades,
    taker_buy_base_asset_volume = excluded.taker_buy_base_asset_volume,
    taker_buy_quote_asset_volume = excluded.taker_buy_quote_asset_volume;
"""
    print(sql)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    row_count = cur.rowcount
    cur.close()
    return query_values,row_count

def lambda_handler(event, context):
    next_fetch = get_latest_epoch()
    
    crawl_records = {r[0]:crawl_data(r[1],r[2]) for r in next_fetch}
    query_values,row_count = insert_data(crawl_records)

    return {
        'statusCode': 200,
        'body': json.dumps({"row_count":row_count, "query_values":query_values})
    }