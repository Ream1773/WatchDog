import logging
import os

# TODO:: Implement the hasher function to make the program more genuine.
# TODO:: Add feature that shows if the directory is empty.


class WatchDog:
    """
    Main class that scans files recursively of provided path
    and logs changes made to them.
    """

    def __init__(self, path: str, logg: logging.Logger):
        self.path = path
        self.logg = logg
        self.is_first_run = True
        self.entities = {}

    def get_tree(self):
        self.is_first_run = True
        while True:
            self._get_entities()
            self.is_first_run = False

    def _get_entities(self):
        """
        Calls the _get_timestamps class method which then scans all the
        elements of the given path parameter.
        :return: -> None
        """
        walk_files = dict()
        for root, dirs, files in os.walk(self.path):
            walk_files.update({os.path.join(root, name): 'Directory' for name in dirs})
            walk_files.update({os.path.join(root, name): 'File' for name in files})

        self._check_existence(walk_files)

    def _check_existence(self, walk_files):
        """
        * Checks if entity is a file or directory.
        * Checks if the file/dir exists and creates modification time if file/dir exists.
        """

        for file in list(self.entities.keys()):
            if file not in walk_files.keys():
                self.logg.info(f"[-] {file} deleted!")
                self.entities.pop(file, None)

        for keys, file_type in walk_files.items():
            try:
                stat = os.stat(keys)
            except FileNotFoundError:
                self.entities.pop(keys, None)
                self.logg.info(f"[-]: {file_type} [-] {keys} deleted!")
                continue

            mod_time = stat.st_mtime
            creation_time = stat.st_ctime
            self._check_changed(keys, mod_time, creation_time, file_type)

    def _check_changed(self, keys, mod_time, creation_time, file_type):
        """
        :param -> keys: File/Directory name
        :param -> mod_time: Modification time
        :param -> creation_time: Creation time
        :param -> file_type: Either directory or File
        :return:
        """
        log_text = str()

        if keys in self.entities:
            if self.entities[keys] != mod_time:
                log_text = f"[+] {file_type} [+]: {keys} modified at {self.entities[keys]}!"
                self.entities[keys] = mod_time
        else:
            self.entities[keys] = mod_time
            log_text = f"[+] NEW {file_type} [+]: {keys} added at {creation_time}!"

        if not self.is_first_run and log_text:
            self.logg.info(log_text)

# class Info:
#     def __init__(self):
#         self.file_info = str()
