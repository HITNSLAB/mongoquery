# API Documentation

### 一、请求参数说明

### 1. 根参数

| 参数      | 类型   | 是否必填 | 描述 | 示例值 | 默认值 |
| :-------- | ------ | -------- | -------- | -------- | --------- |
| operation | String | 是       | 方法名 |createView| - |
| args | dict | 是 | 传给方法的参数，详见各方法的参数列表 |-| - |

- #### operation 方法名

  可选择的取值： `createView`、`dropView`、`dropCollection`、`selectView`、`select`


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

  | 参数       | 类型    | 是否必填 | 描述                                                         | 示例值       | 默认值 |
  | ---------- | ------- | -------- | ------------------------------------------------------------ | ------------ | ------ |
  | collection | String  | 是       | 将进行搜索的集合名称,不可以是视图，且事先必须存在text索引    | onefloor_raw | -      |
  | value      | String  | 是       | text查询的字符串，若value字符串含有空白符，则以空白符分词后返回含有value中全部或部分单词的文档。换句话说，空白符相当于逻辑或 | ddos         | -      |
  | limit      | int     | 否       | 返回的文档数上限值                                           | 100          | None   |
  | page_spec  | dict    | 否       | 分页参数，见详细说明                                         | -            | None   |
  | byyield    | boolean | 否       | 采用yield生成器的方式一次返回一条文档                        | true         | false  |
  | 。。。     | 。。。  | 否       | 见任意参数说明                                               | 。。。       | 。。。 |

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

  | 参数      | 类型         | 是否必填 | 描述                                  | 示例值 | 默认值 |
  | --------- | ------------ | -------- | ------------------------------------- | ------ | ------ |
  | field     | String       | 是       | 查询字段名，见详细说明                | title  | -      |
  | value     | String、dict | 是       | 见详细说明                            | ddos   | -      |
  | limit     | int          | 否       | 返回的文档数上限值                    | 100    | None   |
  | page_spec | dict         | 否       | 分页参数，见详细说明                  | -      | None   |
  | byyield   | boolean      | 否       | 采用yield生成器的方式一次返回一条文档 | true   | false  |
  | 。。。    | 。。。       | 否       | 见任意参数说明                        | 。。。 | 。。。 |

  #### [详细说明]

  - #### field和value

    **描述**

    field和value的取值应符合[db.collection.find() 官方文档](https://docs.mongodb.com/manual/reference/method/db.collection.find/) 中对query参数的field和value要求。

    所有符合mongo语法的value值都可使用

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

    分页参数，类型为字典dict，包含两个int类型字段`page_index`和`page_size`，若page_spec参数被指定，则必须指定这两个字段的值

    此后每次返回的结果将skip前page_index*page_size数目的文档，每次返回的limit等于page_size

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

    可以传入任意个数本文未说明的在[collection.find()函数参数pymongo官方文档](https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.find)中列出的其它参数 ，类型为string、int、dict等，应符合官方文档要求

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

### 二、完整API请求示例

```json
{
    "operation":"selectView",
    "args":{
        "view":"specialized_ddos_view",
        "field":"title",
        "value":"百川PT",
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

