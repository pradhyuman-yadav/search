import json
import os

class JsonDatabase:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        """Load the existing data from the JSON file."""
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, 'r') as file:
            return json.load(file)

    def save_data(self):
        """Save the current data to the JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get(self, key):
        """Retrieve data by key."""
        return self.data.get(key, None)

    def set(self, key, value):
        """Set or update data by key."""
        self.data[key] = value
        self.save_data()

    def delete(self, key):
        """Delete data by key if it exists."""
        if key in self.data:
            del self.data[key]
            self.save_data()

    def get_all(self):
        """Retrieve all data stored in the JSON file."""
        return self.data
