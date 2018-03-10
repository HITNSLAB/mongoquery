import json
import time
from pprint import pprint

from mongo_settings import MONGO_SETTINGS
from mongoquery import MongoQuery


def example_callback(result):
    data = json.loads(result)
    pprint(data['success'])


if __name__ == '__main__':
    query = MongoQuery(MONGO_SETTINGS)
    # data = {
    #     "operation": "createView",
    #     "args": {
    #         "view": "specialized_tools_view",
    #         "collection": "onefloor_raw",
    #         "value": "工具"
    #     }
    # }

    data = '''
        {
      "operation": "selectView",
      "args": {
        "view": "specialized_ddos_view",
        "field": "title",
        "value": {
          "$regex": "ddos"
        },
        "limit":10
      }
    }
        '''

    t1 = time.time()
    for i in range(100):
        # 同步版本
        # ret=json.loads(query.query(data))
        # pprint(ret['success'])
        # 异步回调版本
        query.query(data, callback=example_callback)

    query.threadpool.close()
    query.threadpool.join()

    pprint(time.time() - t1)
