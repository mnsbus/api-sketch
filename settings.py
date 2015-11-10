from multiprocessing import cpu_count
import pytz

ACCELERATION_INTERVAL = 15*60

APIKEY = ''

ACCELERANDS_DOMAINS = 'accelerands_domains'
ACCELERANDS_NUM_WANTED = 100
ACCELERANDS_PING = 'accelerands_ping'

DOMAINS_URL = ''
DOMAINS_MOST_RECENT = 'domains_most_recent'
DOMAINS_INTERVAL = 60 # seconds
DOMAINS_MAX_PER_CHANNEL = 100 # could probably be many more


HOSTNAME = 'localhost' # FAKED: has to be one distributed thing

MAX_PROCESSES = cpu_count()

pageS_BASE_URL = 'http://api.chartbeat.com/live/pages'
pageS_DOMAINS = 'pages_domains'
pageS_FIELDS = tuple(sorted(['domain', 'i', 'path', 'timestamp', 'visitors']))
pageS_PAGE_LIMIT = 100
pageS_MAX_PER_CHANNEL = 100 # have to test/titrate also
pageS_PING = 'pages_ping'
pageS_TABLE = 'visitors'

SQLITE3_FILENAME = 'pages'

UTC = pytz.timezone('UTC')








