from pymongo import MongoClient

class DBModel:

	client = MongoClient()

	def insert_cleaning_data(self, database, collection, documents):
		db = self.client[database]
		results = db[collection].insert_many(documents)

		return results.inserted_ids