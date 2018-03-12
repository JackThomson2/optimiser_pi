import os
import json
from reader import DataStore

STORAGE_LOCATION = './RECORDINGS'

class store_manager:

    # Used to retrieve all the files which have been stored from recordings
    @staticmethod
    def get_files():
        return [entry for entry in os.scandir(STORAGE_LOCATION) if entry.is_file()]

    # Used as an easy way to read the number of recordings made
    @staticmethod
    def get_file_count():
        return len(store_manager.get_files())

    # Store a recording to the directory
    @staticmethod
    def store_file(recording):
        location = STORAGE_LOCATION + '/' + recording['name'] + '.susp'
        with open(location, 'w') as outfile:
            json.dump(recording, outfile)

    # Gets the object from a file name
    @staticmethod
    def get_reader_from_name(name):
        raw_data = json.load(open(name))

        return DataStore.store_from_data(raw_data)