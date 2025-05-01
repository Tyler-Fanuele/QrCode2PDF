class ItemDetails:
    def __init__(self, schema):
        self.details = {str(element[0]):None for element in schema}

    def updateFromDatabaseResults(self, results):
        if len(results) != len(self.details):
            raise ValueError("Number of results does not match number of details")
        for i, key in enumerate(self.details):
            self.details[key] = results[i]

    def __getattr__(self, name):    
        if name in self.details:
            return self.details[name]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def json(self):
        print("ItemDetails::json details dict = ",self.details)
        return self.details