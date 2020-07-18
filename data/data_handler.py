import json
import threading

global_lock = threading.Lock()

class data_handler():
    @staticmethod
    def load(file):
        try:
            with open(f"data/{file}.json", 'r') as f:
                return json.load(f)
        except OSError:
            return data_handler.__handleMissingFile__(file)
        except:
            return None

    @staticmethod
    def dump(data, file):
        try:
            while global_lock.locked():
                continue

            global_lock.acquire()
            with open(f"data/{file}.json", 'w') as f:
                json.dump(data, f, indent = 4)
        except:
            raise
        finally:
            global_lock.release()

    @staticmethod
    def __handleMissingFile__(file):
        try:
            with open(f"data/{file}.json.example", 'r') as f:
                example = json.load(f)

            data_handler.dump(example, file)
            return data_handler.load(file)
        except:
            return None
