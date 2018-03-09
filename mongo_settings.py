MONGO_SETTINGS = {
    "hosts": [
        '172.26.253.140',
        '172.26.253.141',
        '172.26.253.142'
    ],
    "user": 'manager-rw',
    'password': 'HITdbManager-rw!',
    'dbname': 'ti_grey_site_post_event',
    'colname': 'onefloor_raw',
    'options': {
        'replicaset': 'nistmain',
        'readPreference': 'secondary',
        'w': "majority"
    }
}
