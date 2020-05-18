# Commands
PING_COMMAND = 'ping'
PING_COUNT_OPTION = '-c'
PING_QUIET_COMMAND = '-q'

# Prefixes and suffixes
WWW_PREFIX = 'www.'
COM_SUFFIX = '.com'

# Delimiter
PERIOD_DELIMITER = '.'
SPACE_DELIMITER = ' '

# Hosts
GOOGLE_HOSTNAME = 'google'
APPLE_HOSTNAME = 'apple'
LOCAL_ROUTER = '192.168.86.1'

# Max Values
MAX_ACCEPTABLE_PACKET_LOSS = 3
MAX_ACCEPTABLE_AVERAGE_ROUND_TRIP_TIME = 40

# Command exit error
COMMAND_EXIT_ERROR_MESSAGE = 'returned non-zero exit status'

# Error log messages
LOCAL_ROUTER_ERROR = 'Cannot connect to local router'
RESOLVE_HOST_ERROR = 'Cannot connect to internet: Unable to resolve host'
PACKET_LOSS_ERROR = '% packet loss'
ROUND_TRIP_TIME_ERROR = ' ms average round trip time'

# Parsed response dictionary keys
RESPONSE_KEY_HOST = 'host'
RESPONSE_KEY_NUM_PACKETS_SENT = 'num_packets_sent'
RESPONSE_KEY_PACKET_LOSS_PERCENT = 'packet_loss_percent'
RESPONSE_KEY_MAX_ROUND_TRIP_TIME = 'max_round_trip_time'
RESPONSE_KEY_AVERAGE_ROUND_TRIP_TIME = 'average_round_trip_time'
RESPONSE_KEY_ABLE_TO_RESOLVE_HOST = 'able_to_resolve_host'
RESPONSE_KEY_ERROR = 'error'
