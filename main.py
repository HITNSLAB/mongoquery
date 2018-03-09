from mongo_settings import MONGO_SETTINGS
from mongoquery import MongoQuery

if __name__ == '__main__':
    query = MongoQuery(MONGO_SETTINGS)
    dict_data = {
        "operation": "selectView",
        "args": {
            "view": "specialized_ddos_view",
            "field": "title",
            "value": "百川PT",
            "page_spec": {
                "page_index": 4,
                "page_size": 100
            },
            "sort": {
                "postdate": -1
            }
        }
    }
    query.query(dict_data)
