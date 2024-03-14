import os
import yaml


class FileManager:
    def write_to_file(self, directory, filename, data):
        with open(os.path.join(directory, filename), "w") as file:
            yaml.dump(data, file)

    def read_from_file(self, directory, filename):
        with open(os.path.join(directory, filename), "r") as file:
            return yaml.safe_load(file)
