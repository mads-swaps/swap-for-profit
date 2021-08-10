import json
import urllib3
import boto3
import os
import uuid
import psycopg2

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

sqs = boto3.client('sqs', region_name='ap-southeast-1')


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
        where pair_id >= 0
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
    resp = http.request("GET", f"https://www.binance.com/api/v1/klines?symbol={symbol}&interval=15m&limit=20&startTime={epoch}000")
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
    query_values = ",\n    ".join(sql_values)

    reverse_sql_values = []
    for pid,rows in records.items():
        for i,r in enumerate(rows[::-1]):
            r[1] = 1/r[1]
            r[2] = 1/r[2]
            r[3] = 1/r[3]
            r[4] = 1/r[4]
            fields = [str(pid*-1-1)] + [str(f) for f in r][:-1]
            fields[1] = f"to_timestamp({fields[1][:-3]})"
            fields[7] = f"to_timestamp({fields[7][:-3]})"
            if i == 0:
                fields[7] = "NULL"
            reverse_sql_values.append("(" + (",".join(fields)) + ")")
    reverse_query_values = ",\n    ".join(reverse_sql_values)

    if len(sql_values) == 0:
        return "",-1

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
    # print(query_values)
    cur = conn.cursor()
    cur.execute(sql)

    sql = f"""
insert into candlestick_15m (pair_id, open_time, "open", low, high, "close", quote_asset_volume, close_time,
    volume, number_of_trades, taker_buy_quote_asset_volume, taker_buy_base_asset_volume)
values
    {reverse_query_values}
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
    # print(query_values)
    cur.execute(sql)

    conn.commit()
    row_count = cur.rowcount
    cur.close()
    return query_values,row_count

def queue_for_pairs(pairs_list):
    print(pairs_list)
    if len(pairs_list) > 0:
        pairs_str = ",".join([str(s) for s in pairs_list])
        sql = f"""select s.id from environment e join simulation s on s.environment_id=e.id where pair_id in ({pairs_str}) and s.active = true"""
        print(sql)
        cur = conn.cursor()
        cur.execute(sql)
        r = cur.fetchall()
        cur.close()

        sqs_messages = [{'Id':f"{row[0]}",'MessageBody':f"{row[0]}", 'MessageGroupId':"group", 'MessageDeduplicationId':uuid.uuid4().hex.upper()} for row in r]
        n = 10
        sqs_batches = [sqs_messages[i * n:(i + 1) * n] for i in range((len(sqs_messages) + n - 1) // n )]
        for sqs_batch in sqs_batches:
            print(sqs_batch)
            sqs.send_message_batch(QueueUrl='https://sqs.ap-southeast-1.amazonaws.com/917786932753/simulation-queue.fifo', Entries=sqs_batch)

def lambda_handler(event, context):
    next_fetch = get_latest_epoch()
    
    crawl_records = {r[0]:crawl_data(r[1],r[2]) for r in next_fetch}
    query_values,row_count = insert_data(crawl_records)

    queue_for_pairs([pid for pid,rows in crawl_records.items() if len(rows) > 1])
    
    return {
        'statusCode': 200,
        'body': json.dumps({"row_count":row_count, "query_values":query_values})
    }