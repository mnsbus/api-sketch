
#from multiprocessing import Process, Queue
import sys
import pandas as pd
from settings import ACCELERANDS_DOMAINS, ACCELERANDS_NUM_WANTED
from settings import ACCELERANDS_PING, ACCELERATION_INTERVAL
from settings import pageS_MAX_PER_CHANNEL, pageS_FIELDS
from utils import create_epoch_timestamp
from sql_access import get_page_data
from redis_access import get_pubsub, pop_n_items


def calculate_visitors_sign(df):
   return df['visitors'] * df['flag']


def divide_by_flag(grouped):
   return grouped['visitors'] / grouped['flag']


def calculate_accelerands(df, ts):
    # TODO: verify
    # TODO: provide actual average rise over interval
    half_interval = ts - (ACCELERATION_INTERVAL / 2)
    df['flag'] = df['timestamp'].map(lambda x: 1 if x > half_interval else -1)
    df['visitors_signed'] =  df.apply(calculate_visitors_sign, axis=1)
    df = df[df['visitors_signed'] > 0] # only rising
    trending = df.groupby('path').sum().sort('visitors_signed',
        ascending=False).head(ACCELERANDS_NUM_WANTED).reset_index()
    trending['avg_visitor_count'] = trending.apply(divide_by_flag, axis=1)
    trending = trending[['path', 'avg_visitor_count']]
    trending = trending.to_dict('records')
    return trending


def publish_accelerands(domain_name, trending):
    # TODO: to redis:
    # rc.set(domain_name, json.dumps(trending))
    sys.stdout.write(domain_name+"\t"+str(trending)+"\n")
    sys.stdout.flush()
    pass


def process_domains(domains):
    ts = int(create_epoch_timestamp())
    start_time = ts - ACCELERATION_INTERVAL
    for domain in domains:
        data = get_page_data(domain, start_time)
        df = pd.DataFrame(data)
        # TODO: check sqlite3's output vs. delivers Python dict.items()
        # but anyway will have to be fixed so changing db server does not
        # lead to errors
        acceleration_minutes = ACCELERATION_INTERVAL / 60
        trending = [{domain: 'Not enough data for %s-minute window'
            % acceleration_minutes}]
        if not df.empty:
            # TODO: revisit
            df.columns = pageS_FIELDS
            moments = pd.unique(df.timestamp.ravel())
            if len(moments) >= acceleration_minutes:
                trending = calculate_accelerands(df, ts)
        publish_accelerands(domain, trending)


def main():
    ps = get_pubsub(ACCELERANDS_PING)
    for notification in ps.listen():
        domains = pop_n_items(ACCELERANDS_DOMAINS, pageS_MAX_PER_CHANNEL)
        print domains
        # TODO: Multiprocessing
        process_domains(domains)



if __name__ == "__main__":
    main()
