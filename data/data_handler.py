import json

class data_handler():
    @staticmethod
    def load(file):
        try:
            return json.load(open(f"data/{file}.json"))
        except:
            return None

    @staticmethod
    def dump(data, file):
        try:
            json.dump(data, open(f"data/{file}.json", 'w'), indent = 4)
        except:
            raise