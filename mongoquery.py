import json
# import logging
from multiprocessing.pool import ThreadPool
from urllib.parse import quote_plus

from bson import json_util
from pymongo import MongoClient


class MongoQuery(object):
    def __init__(self, settings):
        _uris = [
            "mongodb://%s:%s@%s/" % (
                quote_plus(settings['user']),
                quote_plus(settings['password']),
                quote_plus(host)) for host in settings['hosts']
        ]
        self.connection = MongoClient(
            host=_uris,
            **settings['options']
        )

        self.database = self.connection.get_database(settings['dbname'])
        # self.collection = self.database.get_collection(
        #     settings['colname']
        # )
        self.threadpool = ThreadPool()
        # logging.basicConfig(level=logging.INFO,
        #                     format='%(asctime)s %(levelname)-8s [%(name)s:%(lineno)s] %(message)s',
        #                     datefmt='%Y-%m-%d %H:%M:%S')
        # self.logger = logging.getLogger(__name__)

    def createView(self, view, collection, value):
        self.database.command(
            'create',
            view,
            viewOn=collection,
            pipeline=[
                {
                    '$match': {
                        '$text': {
                            '$search': value
                        }
                    }
                }
            ]
        )

    def dropView(self, view):
        self.dropCollection(view)

    def dropCollection(self, collection):
        self.database.drop_collection(collection)

    def textSearch(self, collection, value, **kwargs):
        return self.select(
            collection=collection,
            field='content',
            value=value,
            is_view=True,
            is_text=True,
            **kwargs
        )

    def selectView(self, **kwargs):
        kwargs['is_view'] = True
        if 'view' in kwargs:
            kwargs['collection'] = kwargs.pop('view')
        return self.select(**kwargs)

    def select(self, collection, field, value, is_view=False, is_text=False, limit=111110, page_spec=None,
               byyield=False,
               **other_options):
        col = self.database[collection]

        matcher = {
            field: value
        }

        if not is_view and (is_text or field == 'content'):
            matcher = {
                '$text': {
                    '$search': value
                }
            }

        found = col.find(
            filter=matcher,
            limit=page_spec['page_size'] if page_spec is not None else limit,
            skip=int(page_spec['page_index']) * int(page_spec['page_size']) if page_spec is not None else 0,
            **other_options
        )
        return [doc for doc in found]

    def query(self, param, to_json=False, callback=None):
        if isinstance(param, str):
            param = json.loads(param)

        operation = getattr(self, param['operation'], None)
        if operation is not None:
            if callback is not None:
                self.threadpool.apply_async(operation, kwds=param['args'], callback=callback)

            else:
                ret = operation(**param['args'])
                if to_json:
                    ret = json_util.dumps(ret)
                return ret
        else:
            raise KeyError("Operation not found")

    # @staticmethod
    # def _fix_encode(obj):
    #     for it in MongoQuery._recursive_iter(obj):
    #         if isinstance(it,str):
    #             try:
    #                 pprint("ggggg")
    #                 pprint(it)
    #             except Exception as e:
    #                 print(e.with_traceback(e))
    #
    # @staticmethod
    # def _recursive_iter(obj):
    #     if isinstance(obj, dict):
    #         for item in obj.values():
    #             yield from MongoQuery._recursive_iter(item)
    #     elif any(isinstance(obj, t) for t in (list, tuple)):
    #         for item in obj:
    #             yield from MongoQuery._recursive_iter(item)
    #     else:
    #         yield obj
