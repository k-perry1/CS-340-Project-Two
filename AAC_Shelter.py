from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient. Provides accesss to database and collections
        self.client = MongoClient('mongodb://%s:%s@127.0.0.1:52999/AAC' % (username, password))
        # where xxxx is your unique port number
        self.database = self.client['AAC']

    # Method that creates and inserts a docuement into database
    def create(self, data):
        if data is not None:
            if type(data) is dict: # Checks that data is in dictionary format
                self.database.animals.insert(data) 
                return True
            else:
                return False
        else:
            return False

    # A method to implement the R in CRUD. 
    def read(self, value):
        if value is not None:
            cursor = self.database.animals.find(value, {"_id": False})
            return cursor
        else:
            raise Exception("Nothing to search, value parameter is empty")
          
    # A method for updating document(s)
    def update(self, value, new_value):
        # Check that parameters are valid, else return error
        if value or new_value is not None:
            result = self.database.animals.update_many(value, { "$set": new_value }) # Updates document, stores in result
            # Return errors if unable to update document
            if result.matched_count == 0:
                return "Error: Cannot update, no matching document found"
            if result.modified_count == 0:
                return "Error: No changes to documents needed"
            # Returns result of updates
            return result.raw_result
        else:
            raise Exception ("Error: search key or update is empty")
            
    # A method for removing document(s) from database
    def delete(self, value):
        # Check that parameters are valid, else return error
        if value is not None:
            result = self.database.animals.delete_many(value) # Delete matching documents
            if result.deleted_count == 0:    # If no documents matched conditions, return message
                return "No matching documents to delete"
            return result.raw_result # Return result of deletion
        else: 
            raise Exception("Error: nothing to delete, value parameter is empty")
          
           