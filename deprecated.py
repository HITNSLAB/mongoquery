# coding=utf-8
import re
import sys

from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf-8')

# 这个是master
mongo = MongoClient('172.26.253.141', 27017)
# 这是针对单个数据库的认证，直接连接词数据库，用此数据库的用户，还有全局的用户
db_auth = mongo.admin
db_auth.authenticate("manager-rw", "HITdbManager-rw!")
db = mongo['ti_grey_site_post_event']
collection = db['onefloor_raw']

# print ("Number of Documents: ")
# print (collection.find().count())


'''
通过关键词直接查询content字段,一次性返回所有数据,返回的是列表,列表的每个条目是一条数据
'''


def select(keyword):
    docs = []
    for doc in collection.find({"content": re.compile(keyword)}):
        docs.append(doc)
    return docs


'''
通过关键词直接查询content字段,每次返回一条数据
'''


def select_(keyword):
    for doc in collection.find({"content": re.compile(keyword)}):
        yield doc


# 调用方式
# docs = select_("注册表")
# while docs.next():
#     doc = docs.next()
#     print doc

'''
通过关键词分页查询content字段,pageIndex是页面索引,pageSize是页面大小,每次返回当前页的所有数据
'''


def select_fenye(keyword, pageIndex, pageSize):
    docs = []
    for doc in collection.find({"content": re.compile(keyword)}).skip(pageIndex * pageSize).limit(pageSize):
        docs.append(doc)
    return docs


'''
在视图查询关键词,viewName视图名称,keyword关键词,一次性返回所有数据
'''


def selectFromView(viewName, keyword):
    coll = db[viewName]
    docs = []
    for doc in coll.find({"content": re.compile(keyword)}):
        docs.append(doc)
    return docs


'''
在视图查询关键词,viewName视图名称,keyword关键词,每次返回一条数据
'''


def selectFromView_(viewName, keyword):
    coll = db[viewName]
    for doc in coll.find({"content": re.compile(keyword)}):
        yield doc


# docs = selectFromView("注册表_View","小月月上海行")
# for doc in docs:
#     print doc

'''根据关键词创建视图,viewname视图名称'''


def createview(viewName, keyword):
    db.command(
        'create',
        viewName,
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


# createview("注册表View","注册表")
# coll = db['注册表View']
# print str(coll.find().count())

'''删除视图,参数:视图名称'''


def dropView(viewName):
    db.command('drop', viewName)

# dropView("注册表View")
