import os

class FileUtils:
    def __init__(self, path):
        self.file_list = []
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.abspath(os.path.join(dirpath, filename))
                filesize = os.path.getsize(filepath)
                filedate = os.path.getctime(filepath)
                self.file_list.append({'filename':filename, 'filesize':filesize, 'filedate':filedate, 'filepath':filepath})
    def get_file_list(self):
        return self.file_list