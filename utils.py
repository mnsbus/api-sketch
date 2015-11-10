import arrow

def create_epoch_timestamp():
    a = arrow.now()
    utc = a.to("UTC")
    return utc.timestamp
