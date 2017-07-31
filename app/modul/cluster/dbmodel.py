from pymongo import MongoClient

class DBModel:

	client = MongoClient()

	def get_data_all(self, database, collection):
		db = self.client[database]
		cursor = db[collection].find({})

		return cursor

	def insert_many(self, database, collection, documents):
		db = self.client[database]
		db[collection].drop()
		results = db[collection].insert_many(documents.to_dict('records'))

		return results.inserted_ids

	def insert_one(self, database, collection, documents):
		db = self.client[database]
		results = db[collection].insert(documents)

		return results

	def drop_collection(self, database, collection):
		db = self.client[database]
		results = db[collection].drop()

		return results
