import json
# import logging
from multiprocessing.pool import ThreadPool
from urllib.parse import quote_plus

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

    def select(self, collection, field, value, is_view=False, is_text=False, limit=None, page_spec=None, byyield=False,
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
            skip=int(page_spec['page_index']) * int(page_spec['page_size']) if page_spec is not None else None,
            **other_options
        )

        if byyield:
            for doc in found:
                yield doc
        else:
            return [doc for doc in found]

    def query(self, param, to_json=False, callback=None):
        operation = getattr(self, param['operation'], None)
        if operation is not None:
            if callback is not None:
                self.threadpool.apply_async(operation, kwds=param['args'], callback=callback)

            else:
                ret = operation(**param['args'])
                if to_json:
                    ret = json.dumps(ret)
                return ret
        else:
            raise KeyError("Operation not found")
