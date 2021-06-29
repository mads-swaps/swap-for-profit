def secrets():
    return {"host": "",
            "port": 5432,
            "database": "",
            "user": "",
            "pass": ""}

def psycopg2(secrets) :
     return ('dbname='+secrets['database']+' user='+secrets['user']+
        ' password='+secrets['pass']+' host='+secrets['host']+
        ' port='+str(secrets['port']))
