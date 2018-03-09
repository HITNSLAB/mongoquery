from urllib.parse import quote_plus

from pymongo import MongoClient
import logging


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
        self.collection = self.database.get_collection(
            settings['colname']
        )
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)-8s [%(name)s:%(lineno)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)

    def createView(self, view, keyword):
        self.database.command(
            'create',
            view,
            viewOn='onefloor_raw',
            pipeline=[
                {
                    '$match': {
                        '$text': {
                            '$search': keyword
                        }
                    }
                }
            ]
        )

    def dropView(self, viewName):
        self.database.command('drop', viewName)

    def selectFromView(self, view, field, keyword, is_regex=False, limit=None, ):
        pass
