import json
from multiprocessing.pool import ThreadPool
from urllib.parse import quote_plus

from bson import json_util
from pymongo import MongoClient


class MongoQuery(object):
    _threadpool = None

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
        if MongoQuery._threadpool is None:
            MongoQuery._threadpool = ThreadPool()

    @property
    def threadpool(self):
        return MongoQuery._threadpool

    def createView(self, view, collection, value):
        return self.database.command(
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
        return self.dropCollection(view)

    def dropCollection(self, collection):
        return self.database.drop_collection(collection)

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

    def select(self, collection, field, value, is_view=False, is_text=False, limit=None, page_spec=None,
               **other_options):
        col = self.database[collection]
        param = {}
        param['filter'] = {
            field: value
        }
        if 'sort' in other_options:
            other_options['sort'] = list(other_options['sort'].items())

        if not is_view and (is_text or field == 'content'):
            param['filter'] = {
                '$text': {
                    '$search': value
                }
            }
        if limit is not None:
            param['limit'] = limit
        if page_spec is not None:
            param['skip'] = int(page_spec['page_index']) * int(page_spec['page_size'])
        found = col.find(**param, **other_options)
        return [doc for doc in found]

    def query(self, *args, callback=None, **kwargs):
        if callable(callback):
            return self.threadpool.apply_async(self._query_sync, args=args, kwds=kwargs, callback=callback)
        else:
            return self._query_sync(*args, **kwargs)

    def _query_sync(self, param=None, to_json=True):
        result = None
        try:
            if param is None:
                raise KeyError("Request cannot be None")
            if isinstance(param, str):
                param = json.loads(param)
            operation = getattr(self, param['operation'], None)
            if operation is None:
                raise KeyError("Operation not found")
            result = operation(**param['args'])
            result = MongoQuery._compose_msg(True, result)
        except Exception as e:
            result = MongoQuery._handle_error(e)
        finally:
            return json_util.dumps(result) if to_json else result

    @staticmethod
    def _handle_error(ex):
        return MongoQuery._compose_msg(False, {
            'exception': type(ex).__name__,
            'msg': str(ex)
        })

    @staticmethod
    def _compose_msg(status, data):
        return {
            'success': status,
            'data': data
        }

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
