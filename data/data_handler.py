import json

class data_handler():
    @staticmethod
    def Load(File):
        try:
            return json.load(open(f"data/{File}.json"))
        except:
            return None

    @staticmethod
    def Dump(Data, File):
        try:
            json.dump(Data, open(f"data/{File}.json", 'w'), indent = 4)
        except:
            raise