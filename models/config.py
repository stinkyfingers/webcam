import json
import os

class Config():
    def __init__(self):
        self.appdir = os.path.join(os.path.expanduser('~'), 'stopmotion')
        if not os.path.isdir(self.appdir):
            os.mkdir(self.appdir)
        self.filename = os.path.join(self.appdir, 'config.json')
        self.data = {
            'appdir': self.appdir
        }
        if not os.path.isfile(self.filename):
            self.write()

    def read(self):
        with open(self.filename, 'r+') as file:
            self.data = json.load(file)

    def write(self):
        with open(self.filename, 'w+') as file:
            json.dump(self.data, file)

    def upsert(self, dict):
        if os.path.isfile(self.filename):
            self.read()
        for k, v in dict.items():
            self.data[k] = v
        self.write()

    def get_project_dir(self):
        self.read()
        if 'project' in self.data:
            return self.data['project']
        return os.path.join(self.appdir, 'new_project') #TODO - open OR create
