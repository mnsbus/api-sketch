from multiprocessing import cpu_count
import pytz

ACCELERATION_INTERVAL = 15*60

APIKEY = '317a25eccba186e0f6b558f45214c0e7'

ACCELERANDS_DOMAINS = 'accelerands_domains'
ACCELERANDS_NUM_WANTED = 100
ACCELERANDS_PING = 'accelerands_ping'

DOMAINS_URL = 'https://s3.amazonaws.com/interview-files/hosts.json'
DOMAINS_MOST_RECENT = 'domains_most_recent'
DOMAINS_INTERVAL = 60 # seconds
DOMAINS_MAX_PER_CHANNEL = 100 # could probably be many more


HOSTNAME = 'localhost' # FAKED: has to be one distributed thing

MAX_PROCESSES = cpu_count()

TOPPAGES_BASE_URL = 'http://api.chartbeat.com/live/toppages'
TOPPAGES_DOMAINS = 'toppages_domains'
TOPPAGES_FIELDS = tuple(sorted(['domain', 'i', 'path', 'timestamp', 'visitors']))
TOPPAGES_PAGE_LIMIT = 100
TOPPAGES_MAX_PER_CHANNEL = 100 # have to test/titrate also
TOPPAGES_PING = 'toppages_ping'
TOPPAGES_TABLE = 'visitors'

SQLITE3_FILENAME = 'toppages'

UTC = pytz.timezone('UTC')








