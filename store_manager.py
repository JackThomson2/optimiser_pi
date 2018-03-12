import os
import json

STORAGE_LOCATION = './RECORDINGS'

class store_manager:

    # Used to retrieve all the files which have been stored from recordings
    @staticmethod
    def get_files():
        return [store for store in os.scandir(STORAGE_LOCATION) is store.is_file()]

    # Used as an easy way to read the number of recordings made
    @staticmethod
    def get_file_count():
        return len(store_manager.get_files())

    # Store a recording to the directory
    @staticmethod
    def store_file(recording):
        location = STORAGE_LOCATION + '/' + recording.name + '.susp'
        with open(location, 'w') as outfile:
            json.dump(recording, outfile)
