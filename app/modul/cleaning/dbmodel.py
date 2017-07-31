from pymongo import MongoClient

class DBModel:

	client = MongoClient()

	def insert_cleaning_data(self, database, collection, documents):
		db = self.client[database]
		db[collection].drop()
		results = db[collection].insert_many(documents.to_dict('records'))

		return results.inserted_ids

	def insert_header(self, database, collection, documents):
		db = self.client[database]
		db[collection].drop()
		results = db[collection].insert(documents)

		return results