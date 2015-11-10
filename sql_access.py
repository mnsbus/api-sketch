import sqlite3
#import psycopg2
from settings import ACCELERATION_INTERVAL, SQLITE3_FILENAME
from settings import TOPPAGES_FIELDS, TOPPAGES_TABLE
from utils import create_epoch_timestamp

sqlc = sqlite3.connect(SQLITE3_FILENAME)


def create_values(documents):
    return [tuple([doc[k] for k in sorted(doc)]) for doc in documents]


def make_question_marks(fields):
    return tuple('?' * len(fields))


def make_executemany_string(table, fields):
    qm = make_question_marks(fields)
    insert_string = """INSERT INTO %s %s VALUES %s""" % (table,
        str(fields).replace("'", ''), str(qm).replace("'", ''))
    return insert_string


def calculcate_half_lookback():
    now = create_epoch_timestamp()
    lookback = now - ( ACCELERATION_INTERVAL / 2 )
    return lookback


def get_toppage_data(domain, start_time, list_wanted=True):
    query = """SELECT * FROM visitors WHERE timestamp > {st} AND domain = '{dn}'""".format(st=start_time, dn=domain)
    data = sqlc.execute(query)
    if list_wanted == True:
        data = list(data)
    return data


def write_toppage_records(documents):
    records = create_values(documents)
    es = make_executemany_string(TOPPAGES_TABLE, TOPPAGES_FIELDS)
    sqlc.executemany(es, records)
    sqlc.commit()

# def get_postgres_connection(connection_string="dbname=mns user=mns"):
#     conn = psycopg2.connect(connection_string)
#     cur = conn.cursor()
#     return conn, cur
