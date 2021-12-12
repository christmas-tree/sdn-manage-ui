ODL_CREDS = {
    'username': 'admin',
    'password': 'admin',
}

# Base URLs for Config and operational
BASE_URL = 'http://192.168.56.105:8181'

CONF_URL = '/restconf/config'
OPERATION_URL = '/restconf/operational'

# Specific REST URLs
# nodesUrl = '/opendaylight-inventory:nodes'
# tableUrl = '/flow-node-inventory:table/0'

SUCCESS = 0
UNKNOWN_CMD = 1
BAD_ARG = 2
EXIT = 3
FAILED = 4
PATH_NOT_FOUND = 5
