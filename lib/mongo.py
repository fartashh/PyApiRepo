
import pymongo
import abc
import copy

class Data_Mediator(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        pass
    pass

class Mongo_DataProvider(Data_Mediator):
    def __init__(self):
        super(Mongo_DataProvider, self).__init__()
        self.__is_connected = False
        self.__db = None
        self.__name = ""
        self.__connection = None
        self.__collections = []
        #'profiles', 'profile', 'facebook_profile','twitter_profile', 'votes', 'tweakers', 'tweaks', 'status', 'tags', 'settings', 'last_acts', 'invites', 'sessions', 'suggests']
        #self.__collections__spec = [{"name":'profiles', 'capped':false, siz 'profile', 'votes', 'tweakers', 'tweaks']


    def connect(self, db_name = "_test", collection_names = [],  is_capped = False):
        self.__name = db_name
        self.__connection = pymongo.MongoClient()
        self.__is_connected = True
        self.__db = self.__connection[db_name]
        self.__collections = collection_names if len(collection_names) != 0 else self.__collections
        for col_name in self.__collections:
            if col_name not in self.__db.collection_names():
                if not is_capped:
                    self.__db.create_collection(col_name)
                else:
                    self.__db.create_collection(col_name, **{"capped":True, "size": 100000})
        print "Database {0} is connected".format(db_name)


    def clear_all(self):
        for db_name in self.__collections:
            self.__db[db_name].remove()

    @property
    def db(self):
        return self.__db #if self.__is_connected and hasattr(self, '__db') else None;

    def disconnect(self):
        self.__connection.close()
        self.__is_connected = False
        print "Database {0} is disconnected".format(self.__name)

    def get_collection(self, collection_name):
        #assert ( collection_name in self.__collections), "There is no collection as [" + collection_name+ "]"
        return self.__db[collection_name] #if self.__is_connected and hasattr(self, '__db') else None

    def query(self, collection_name, index = None, criteria = None, sorted_tag = None, exclude_removed = True, limit = 0, skip = 0 ):
        index = index if index else []
        criteria = criteria if criteria else {}
        sorted_tag = sorted_tag if sorted_tag else []
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        collection = self.get_collection(collection_name)
        self.create_index(collection_name, index)
        #if index != []:
        #    collection.ensure_index(index, name = "idx")
        #    #collection.create_index(index, name = "idx")
        if exclude_removed: criteria["isdel"] = False
        cursor = collection.find(criteria).skip(skip).limit(limit) if len(sorted_tag) == 0 else collection.find(criteria).sort(sorted_tag).skip(skip).limit(limit)
        #if index != []:
        #    try:
        #        collection.drop_index("idx")
        #    except:
        #        pass
        return cursor

    def remove_by_index(self, collection_name, criteria = {}, list_field_name = '', index = 0):
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        collection = self.get_collection(collection_name)
        res = collection.update(criteria, {'$unset': {'%s.%d' % (list_field_name, index) : 1}})
        if res['err'] == None:
            res = collection.update(criteria, {'$pull': {list_field_name: None}})
            return res
        return None

    def remove_real(self, collection_name, criteria = {}):
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        collection = self.get_collection(collection_name)
        return collection.remove(criteria)

    def pull(self, collection_name, criteria = {}, pull_criteria={}):
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        collection = self.get_collection(collection_name)
        collection = collection.update(criteria, {"$pull": pull_criteria})
        return collection.remove(criteria)

    def query_gen(self, collection_name, index = None, criteria = None, sorted_tag = None, projection = None, exclude_removed = True, limit = 0, skip = 0 ):
        index = index if index else []
        criteria = criteria if criteria else {}
        sorted_tag = sorted_tag if sorted_tag else []
        projection = projection if projection else {}
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        collection = self.get_collection(collection_name)
        self.create_index(collection_name, index)
        #if index != []:
        #    collection.ensure_index(index, name = "idx")
        #    #collection.create_index(index, name = "idx")
        if exclude_removed: criteria["is_del"] = {'$exists':False}
        if projection == {}:
            cursor = collection.find(criteria).skip(skip).limit(limit) if len(sorted_tag) == 0 else collection.find(criteria).sort(sorted_tag).skip(skip).limit(limit)
        else:
            cursor = collection.find(criteria, projection).skip(skip).limit(limit) if len(sorted_tag) == 0 else collection.find(criteria, projection).sort(sorted_tag).skip(skip).limit(limit)
        count = cursor.count()
        yield count
        for doc in cursor:
            # doc.pop('_id', 0)
            yield doc
        #if index != []:
        #    collection.drop_index("idx")


    def query_script(self, collection_name, index = None, script = "", sorted_tag = None, projection = None, exclude_removed = True, limit = 0, skip = 0 ):
        index = index if index else []
        sorted_tag = sorted_tag if sorted_tag else []
        projection = projection if projection else {}
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        collection = self.get_collection(collection_name)
        criteria = {}
        self.create_index(collection_name, index)
        #if index != []:
        #    collection.ensure_index(index, name = "idx")
        #    #collection.create_index(index, name = "idx")
        if exclude_removed: criteria["isdel"] = False
        criteria['$where'] = script
        if projection == {}:
            cursor = collection.find( criteria ).skip(skip).limit(limit) if len(sorted_tag) == 0 else collection.find(criteria).sort(sorted_tag).skip(skip).limit(limit)
        else:
            cursor = collection.find(criteria , projection).skip(skip).limit(limit) if len(sorted_tag) == 0 else collection.find(criteria , projection).sort(sorted_tag).skip(skip).limit(limit)
        count = cursor.count()
        yield count
        for doc in cursor:
            doc.pop('_id', 0)
            yield doc
        #if index != []:
        #    collection.drop_index("idx")

    def remove_all(self, collection_name):
        self.db[collection_name].remove()

    def create_index(self, collection_name, indexes = None, is_cached = True):
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        indexes = indexes if indexes else []
        index_name = '_'.join([x[0] for x in indexes]).lower()
        collection = self.get_collection(collection_name)
        if indexes != []:
            if index_name not in collection.index_information().keys():
                if is_cached:
                    collection.ensure_index(indexes, cache_for = 300,  name = index_name)
                else:
                    collection.create_index(indexes, name = index_name)

    def query_object(self, classtype, collection_name, index = None, criteria = None):
        index = index if index else []
        criteria = criteria if criteria else {}
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        assert (hasattr(classtype, "__call__")), classtype.__name__ + " is not a class type"
        collection = self.get_collection(collection_name)
        self.create_index(collection_name, index)
        #if index != []:
        #    index_name = '_'.join([x[0] for x in index]).lower()
        #    if index_name not in collection.index_information().keys():
        #        collection.ensure_index(index, name = index_name)
        #        #collection.create_index(index)
        result = []
        for doc in collection.find(criteria):
            temp = classtype()
            for prop, value in doc.iteritems():
                if hasattr(temp, prop):
                    setattr(temp, prop, value)
            result.append(temp)
        return result


    def query_to_instance(self, classtype, collection_name, index = [], criteria = {}, sorted_tag = [], projection = [], exclude_removed = True, limit = 0, skip = 0 ):
        """
        Generates and returns an iterator based on a cursor over given query parameters, and instead of returning dictionary, for each document an instance of given class type will be created and returned
        classtype: Output instance class type e.g. Student, Book, Post, Comment
        collection_name: DB collection name
        index: list of DB indexes to improve query performance e.g. [('twiiq id', ASCENDING), ('date', DESCENDING),...]
        criteria: query where cluase e.g. {'id' : '3423', ...}
        sorted_tag = order by for the generated query which is similar to index parameter
        projection: indicated thoses intrested field in output result {'email':1, 'id':1,...}
        exclude_removed: (True|False) Indicated whether {"isdel":False} criteria should be added by default to query or not
        limit: query result record number limit
        skip: used for paging and says how many record from the first must be skiped
        """
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        collection = self.get_collection(collection_name)
        if index != []:
            collection.create_index(index, name = "idx")
        if exclude_removed: criteria["isdel"] = False
        if projection == {}:
            cursor = collection.find(criteria).skip(skip).limit(limit) if len(sorted_tag) == 0 else collection.find(criteria).sort(sorted_tag).skip(skip).limit(limit)
        else:
            pr = {x:1 for x in projection}
            pr['_id'] = 0
            cursor = collection.find(criteria, pr).skip(skip).limit(limit) if len(sorted_tag) == 0 else collection.find(criteria, projection).sort(sorted_tag).skip(skip).limit(limit)
        count = cursor.count()
        yield count
        for doc in cursor:
            temp = classtype()
            for prop, value in doc.iteritems():
                if hasattr(temp, prop):
                    setattr(temp, prop, value)
            yield temp
        if index != []:
            collection.drop_index("idx")

#shared.DB.db.articles.ensure_index([('abstract','text'), ('title','text'), ('keywords','text')])
        #shared.DB.db.command('text','articles', search = 'text')

    def text_search(self, collection_name, index = None, search_text = '',user_id='', criteria = None, sorted_tag = None, projection = None, exclude_removed = True, limit = 0, skip = 0):
        index = index if index else {}
        sorted_tag = sorted_tag if sorted_tag else []
        criteria = criteria if criteria else {}
        projection = projection if projection else {}
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        collection = self.get_collection(collection_name)

        indexes=[(i,'text') for i in index]

        if([x for x in index if x not in  "".join(collection.index_information().keys())]):
            collection.drop_indexes()
            try:
                collection.create_index(indexes)
            except Exception,e:
                print("{}".format(e))


        if exclude_removed: criteria["is_del"] = {'$exists':False}
        if projection == {}:
            cursor = collection.find({'$text':{'$search':search_text},'is_private':False},{'score':{'$meta':'textScore'}}).skip(skip).limit(limit) if len(sorted_tag) == 0 else collection.find(criteria).sort(sorted_tag).skip(skip).limit(limit)
        else:
            # cursor = collection.find({'$text':{'$search':search_text}},projection).skip(skip).limit(limit) if len(sorted_tag) == 0 else collection.find(criteria, projection).sort(sorted_tag).skip(skip).limit(limit)
            cursor = collection.find({'$text':{'$search':search_text},"$or":[{'is_private':False},{'user_id':user_id}]},projection).skip(skip).limit(limit) if len(sorted_tag) == 0 else collection.find(criteria, projection).sort(sorted_tag).skip(skip).limit(limit)
        count = cursor.count()
        yield count
        for doc in cursor:
            yield doc





        # res = {'results':[]}
        # try_count = 0
        # while try_count < 5:
        #     self.create_index(collection_name, index)
        #     if exclude_removed: criteria["isdel"] = False
        #     try:
        #         ddb = self.__db
        #         res = ddb.command('text',collection_name, search = search_text, filter=criteria, sort = sorted_tag, projection = projection, limit = limit, skip = skip)
        #         break;
        #     except Exception, e:
        #         if 'too many text index for' in str(e):
        #             self.clear_index(collection_name)
        #             try_count +=1
        #         else:
        #             raise e
        # results = res['results']
        # yield len(results)
        # for doc in results:
        #     rec = doc['obj']
        #     rec['text_score'] = doc['score']
        #     rec.pop('_id', 0)
        #     yield rec

    def clear_index(self, collection_name):
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        collection = self.get_collection(collection_name)
        collection.drop_indexes()

    def __byId(self, idStr):
        return pymongo.helpers.bson.ObjectId(idStr)

    def update(self, collection_name, data, update_criteria = {}, isnew = True):
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        #assert (hasattr(data, "DATA_DIC")), data.__name__ + " is not an data object"
        assert (hasattr(data, "__dict__")), data.__name__ + " is not an data object"
        if not hasattr(data, "isdel"):
            setattr(data, "isdel", False)
        collection = self.get_collection(collection_name)
        document = data.__dict__ # self.__normalize_data_dic(data)
        if not isnew:
            return collection.update(update_criteria, document, safe = True) # data.DATA_DIC)
        else:
            res = collection.insert(document, safe = True) # data.DATA_DIC)
            return str(res)

    def update_direct(self, collection_name, where = {}, set_criteria = {}, update_modifier = "$set", create_new = True):
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        # if not where.has_key('isdel'):
        #     where['isdel'] = False
        collection = self.get_collection(collection_name)
        return collection.update(where, { update_modifier :  set_criteria}, multi=True, upsert = create_new)

    def insert_bulk(self, collection_name, collections = None):
        assert (self.__is_connected), "datacontroler is not connected to database, call connect()"
        collection = self.get_collection(collection_name)
        collections = collections if collections else []
        results = []
        if collections != []:
            results.append(collection.insert(collections))
        return  results

    def __normalize_data_dic(self, dic):
        #document = copy.deepcopy(dic)
        del dic['_data_mediator']
        del dic['dm']
        return dic

