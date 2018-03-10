import json
from pprint import pprint

from mongo_settings import MONGO_SETTINGS
from mongoquery import MongoQuery

if __name__ == '__main__':
    query = MongoQuery(MONGO_SETTINGS)
    dict_data = {
        "operation": "selectView",
        "args": {
            "view": "specialized_ddos_view",
            "field": "content",
            "value": {
                "$regex": "^黑客"
            },
            "page_spec": {
                "page_index": 0,
                "page_size": 100
            }
        }
    }
    found = query.query(dict_data, to_json=True)
    pprint(json.loads(found))
