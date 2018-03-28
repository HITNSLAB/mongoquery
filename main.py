import json
import time
from pprint import pprint

from mongo_settings import MONGO_SETTINGS
from mongoquery import MongoQuery


def example_callback(result):
    data = json.loads(result)
    # pprint(data['success'])
    pprint(data)


if __name__ == '__main__':
    query_client = MongoQuery(MONGO_SETTINGS)
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
        "field": "content",
        "value": {
          "$regex": "工具"
        },
        "sort": {
          "obtaintime": -1
        },
        "limit":10
      }
    }
        '''

    t1 = time.time()
    # for i in range(1):
    # 同步版本
    # ret = json.loads(query_client.query(data))
    # pprint(ret['success'])
    # 异步回调版本
    query_client.query(data, callback=example_callback)

    query_client.threadpool.close()
    query_client.threadpool.join()

    pprint(time.time() - t1)
