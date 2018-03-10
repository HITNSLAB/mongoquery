# API Documentation

### 一、请求参数说明

### 1. 根参数

| 参数      | 类型   | 是否必填 | 描述 | 示例值 | 默认值 |
| :-------- | ------ | -------- | -------- | -------- | --------- |
| operation | String | 是       | 方法名 |createView| - |
| args | dict | 是 | 传给方法的参数，详见各方法的参数列表 |-| - |

- #### operation 方法名

  可选择的取值： `createView`、`dropView`、`dropCollection`、`textSearch`、`selectView`、`select`


### 2. args 方法参数

- #### createView

  | 参数       | 类型   | 是否必填 | 描述                              | 示例值                | 默认值 |
  | ---------- | ------ | -------- | --------------------------------- | --------------------- | ------ |
  | view       | String | 是       | 将创建的视图名称                  | specialized_ddos_view | -      |
  | collection | String | 是       | 视图所基于的collection            | onefloor_raw          | -      |
  | value      | String | 是       | 建立视图所根据的content关键字内容 | ddos                  | -      |

- #### dropView

  | 参数 | 类型   | 是否必填 | 描述             | 示例值                | 默认值 |
  | ---- | ------ | -------- | ---------------- | --------------------- | ------ |
  | view | String | 是       | 将销毁的视图名称 | specialized_ddos_view | -      |

- #### dropCollection

  | 参数       | 类型   | 是否必填 | 描述                   | 示例值       | 默认值 |
  | ---------- | ------ | -------- | ---------------------- | ------------ | ------ |
  | collection | String | 是       | 将销毁的collection名称 | onefloor_raw | -      |

- #### textSearch

  | 参数       | 类型   | 是否必填 | 描述                                                         | 示例值       | 默认值 |
  | ---------- | ------ | -------- | ------------------------------------------------------------ | ------------ | ------ |
  | collection | String | 是       | 将进行搜索的集合名称,不可以是视图，且事先必须存在text索引    | onefloor_raw | -      |
  | value      | String | 是       | text查询的字符串，若value字符串含有空白符，则以空白符分词后返回含有value中全部或部分单词的文档。换句话说，空白符相当于逻辑或 | ddos         | -      |
  | limit      | int    | 否       | 返回的文档数上限值                                           | 100          | None   |
  | page_spec  | dict   | 否       | 分页参数，见详细说明                                         | -            | None   |
  | 。。。     | 。。。 | 否       | 见任意参数说明                                               | 。。。       | 。。。 |

  ​

- #### selectView

  | 参数   | 类型   | 是否必填 | 描述                   | 示例值                | 默认值 |
  | ------ | ------ | -------- | ---------------------- | --------------------- | ------ |
  | view   | String | 是       | 将进行搜索的视图名称   | specialized_ddos_view | -      |
  | 。。。 | 。。。 | 。。。   | 详见select通用参数列表 | 。。。                | 。。。 |

- #### select

  | 参数       | 类型    | 是否必填 | 描述                             | 示例值       | 默认值 |
  | ---------- | ------- | -------- | -------------------------------- | ------------ | ------ |
  | collection | String  | 是       | 将进行搜索的集合或视图名称       | onefloor_raw | -      |
  | is_view    | boolean | 否       | collection字段所对应的是否是视图 | false        | false  |
  | 。。。     | 。。。  | 。。。   | 详见select通用参数列表           | 。。。       | 。。。 |

- #### select通用参数

  | 参数      | 类型         | 是否必填 | 描述                   | 示例值 | 默认值 |
  | --------- | ------------ | -------- | ---------------------- | ------ | ------ |
  | field     | String       | 是       | 查询字段名，见详细说明 | title  | -      |
  | value     | String、dict | 是       | 见详细说明             | ddos   | -      |
  | limit     | int          | 否       | 返回的文档数上限值     | 100    | None   |
  | page_spec | dict         | 否       | 分页参数，见详细说明   | -      | None   |
  | 。。。    | 。。。       | 否       | 见任意参数说明         | 。。。 | 。。。 |

  #### [详细说明]

  - #### field和value

    **描述**

    `field`和`value`的取值应符合[db.collection.find() 官方文档](https://docs.mongodb.com/manual/reference/method/db.collection.find/) 中对query参数的field和value要求。

    所有符合mongo语法的`value`值都可使用

    **示例值**

    ```json
    {
        "field":"thread-id",
        "value":{
            "$gt":21
        }
    }
    ```

    ```json
    {
        "field":"username",
        "value":"C0d3r1iu"
    }
    ```

  - #### page_spec

    **描述**

    分页参数，类型为字典dict，包含两个int类型字段`page_index`和`page_size`，若`page_spec`参数被指定，则必须指定这两个字段的值

    此后每次返回的结果将skip前page_index*page_size数目的文档，每次返回的`limit`等于`page_size`

    **示例值**

    ```json
    {
        "page_spec":{
            "page_index":5,
            "page_size":100
        }
    }
    ```

  - #### 任意个数参数

    **描述**

    可以传入任意个数本文未说明的在[collection.find()函数参数pymongo官方文档](https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.find)中列出的其它参数 ，类型为`string`、`int`、`dict`等，应符合官方文档要求

    **示例值**

    ```json
    {
        "projection":{
            "username":1
        },
        "sort":{
            "postdate":1
        }
    }
    ```


  #### [注意事项]

  1. 在非view模式下查询content字段会自动转换为$text搜索，此时value必须为一个字符串，不能为字典

  2. 如果使用value为字符串的方式查询字符串字段，按照Mongo的语义是完全匹配。

     所以如果你需要在title、content查找包含某个字符串的文档，请使用如下方式进行正则匹配

     ```json
     {
         "field":"title",
         "value":{
             "$regex":"百川PT"
         }
     }
     ```

     \$regex匹配将无法使用索引而是直接遍历，因此建议只在view表里使用\$regex，因为view表数据量少。

     如果在原始表里搜的话使用textSearch，或者直接使用`"value":"sss"`进行完全匹配(完全匹配将会使用索引)

  3. 不可以在view表中使用textSearch

### 二、完整API请求示例

```json
{
    "operation":"selectView",
    "args":{
        "view":"specialized_ddos_view",
        "field":"title",
        "value":{
            "$regex":"百川PT"
        },
        "page_spec":{
            "page_index":4,
            "page_size":100
        },
        "sort":{
            "postdate":-1
        }
    }
}
```

### 三、响应格式

| 参数    | 类型    | 是否必填 | 描述         | 示例值 |
| ------- | ------- | -------- | ------------ | ------ |
| success | boolean | 是       | 操作是否成功 | true   |
| data    | dict    | 是       | 见详情       | -      |

- #### data格式

  当`success`为`true`时,`data`的内容为Mongo服务器返回的原始内容

  当`success`为`false`时，将返回一个`dict`，以显示抛出的异常信息

#### 示例相应

```json
{
  "success": false,
  "data": {
    "msg": "a view 'ti_grey_site_post_event.specialized_tools2_view' already exists",
    "exception": "OperationFailure"
  }
}
```

```json
{
  "success": true,
  "data": [
    {
      "acctid": null,
      "id": 66959332,
      "_id": {
        "$oid": "5a7c7b41956e14158c1b827d"
      },
      "otherinfo1": null,
      "content": "黑客快速入门",
      "site": "www.hackyue.com",
      "posttime": {
        "$date": 1357811965000
      },
      "rescount": 0,
      "key_words": "",
      "gmtdate": {
        "$date": 1471305600000
      },
      "otherinfo2": null,
      "username": "admin",
      "content_label": "开发技术讨论",
      "isoriginal": "1",
      "reply_tone": "未明确态度",
      "nickname": null,
      "posthref": "http://www.hackyue.com/forum.php?mod=viewthread&tid=14434&extra=page=116&filter=author&orderby=dateline",
      "title": "黑客快速入门",
      "threadid": "e6348672-bf53-11e6-a1b8-000c2921ef88",
      "siteurl": "www.hackyue.com",
      "postfloor": "1",
      "viewcount": -1,
      "datasource": 1,
      "sitetype": "12",
      "board": "全国技术综合交流"
    }
  ]
}
```

