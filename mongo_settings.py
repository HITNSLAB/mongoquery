MONGO_SETTINGS = {
    "hosts": [
        '10.245.144.92',
        '10.245.144.93',
    ],
    "user": 'manager-rw',
    'password': 'HITdbManager-rw!',
    'dbname': 'threat_info',
    # 'colname': 'onefloor_raw',
    'options': {
        'replicaset': 'nistmain',
        'readPreference': 'secondaryPreferred',
        'w': "majority"
    }
}
