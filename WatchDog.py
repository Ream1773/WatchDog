import os
# TODO:: Delete files from dictionary that are not in the specified path to prevent crashes.
# TODO:: Implement the hasher function to make the program more genuine.


class WatchD:
    """
    Main class that scans files recursively of provided path
    and logs changes made to them.
    """
    def __init__(self, path: str, logg):
        self.path = path
        self.logg = logg
        self.files = {}
        self.dirs = {}
        self.is_first_run = True
        self.file_set = set()

    def get_tree(self):
        self.is_first_run = True
        while True:
            self.get_timestamps(self.path)
            self.is_first_run = False

    def get_timestamps(self, path: str):
        for root, dirs, files in os.walk(path, topdown=True):
            self.check_entities(root, files, False)
            self.check_entities(root, dirs, True)

    def check_entities(self, root, walk_files, is_dir):
        if is_dir:
            db_files = self.dirs
            file_type = "directory"
        else:
            file_type = "file"
            db_files = self.files

        for name in walk_files:
            keys = os.path.join(root, name)
            stamps = os.stat(keys).st_mtime
            self.check_changed(keys, stamps, db_files, file_type)

    def check_changed(self, keys, stamps, db_files, file_type):
        log_text = str()

        if keys in db_files:
            if db_files[keys] != stamps:
                log_text = f"{db_files[keys]} Changed"
                db_files[keys] = stamps
        else:
            db_files[keys] = stamps
            log_text = f"New {file_type} {keys} added!"
            # self.file_set.add(keys)
            print(db_files)

        if not self.is_first_run and log_text:
            self.logg.info(log_text)

    # def deleted_files(self, keys, file_type, db_files):
    #     if self.file_set not in db_files.keys():
    #         log_text = f"{file_type} {keys} deleted from {self.path}"
    #         self.logg.info(log_text)
    #         self.file_set.clear()
