from pymongo import MongoClient
from .config import Config
import logging
from bson.objectid import ObjectId

config = Config()

class HarmonyDatabaseHandler:
    def __init__(self):
        logger = logging.getLogger()
        logger.setLevel(logging.WARNING)
        self.logger = logger
        self.client = MongoClient(config.MONGO_DB_URL)
        self.db = self.client[config.MONGO_DB_NAME]

    def save_collectionList_to_db(self, collection_name, collection_data):
        self.logger.warning("tableName: %s\nData: %s", collection_name, collection_data[0])
        collection = self.db[collection_name]
        try:
            collection.insert_many(collection_data)
        except Exception as ex:
            self.logger.warning('Exception occured: %s', ex)

    def save_collection_to_db(self, collection_name, collection_data):
        self.logger.warning("tableName: %s", collection_name)
        collection = self.db[collection_name]
        try:
            collection.insert_one(collection_data)
        except Exception as ex:
            self.logger.warning('Exception Occured: %s', ex)

    def update_experiment_with_results(self, exp_id, file_key, file_path):
        self.save_experiment_results('experiment', exp_id, {file_key: file_path})

    def save_experiment_results(self, collection_name, exp_id, results):
        current_exp = (self.find_one_by_parameter('id', exp_id, collection_name))
        current_exp['results'] = results
        self.logger.warning("results: %s", results)
        self.update_database(current_exp['id'], current_exp,  collection_name)

    def find_one_by_parameter(self, param, value, collection_name):
        self.logger.warning('find_one_by_parameter: %s %s %s', param, value, collection_name)
        return self.db[collection_name].find_one({param: value})

    def update_database(self, id, element, collection_name):
        self.logger.warning('update : %s %s %s', id, collection_name, element)
        filt = {'_id': ObjectId(id)}
        set_obj = {"$set": element}
        return self.db[collection_name].update_one(filt,set_obj)

