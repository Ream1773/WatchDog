import logging
import os
import hashlib


class WatchDog:

    """
    Main class that scans files recursively of provided path
    and logs changes made within path scope.
    """

    def __init__(self, path: str, logg: logging.Logger):
        self.path = path
        self.logg = logg
        self.is_first_run = True
        self.ts_dict = dict()
        self.hashes = dict()

    def get_tree(self):
        self.is_first_run = True
        while True:
            self._get_entities()
            self.is_first_run = False

    def _get_entities(self):

        """
        Iterates over path and updates the file dict.
        :return: None
        """

        walk_files = dict()

        for root, dirs, files in os.walk(self.path):
            walk_files.update({os.path.join(root, name): 'Directory' for name in dirs})
            walk_files.update({os.path.join(root, name): 'File' for name in files})

        self._check_existence(walk_files)

    def _check_existence(self, walk_files: dict):

        """
        * Checks if item exists:
        * Checks if item is a file or directory.
        * Creates modification time if item exists.
        """

        for file in list(self.ts_dict.keys()):
            if file not in walk_files.keys():
                self.logg.info(f"[-]{file} deleted!")
                self.ts_dict.pop(file, None)
                self.hashes.pop(file, None)

        for keys, file_type in walk_files.items():
            try:
                stat = os.stat(keys)
            except FileNotFoundError:
                self.ts_dict.pop(keys, None)
                self.hashes.pop(keys, None)
                self.logg.info(f"[-]:{file_type}[-] {keys} deleted!")
                continue

            mod_time = stat.st_mtime
            creation_time = stat.st_ctime

            self._check_mod_time(keys, mod_time, creation_time, file_type)

    def _check_mod_time(self, keys: str, mod_time: str, creation_time: str, file_type: str):

        """
        :param keys: File/Directory name
        :param mod_time: Modification time
        :param creation_time: Creation time
        :param file_type: Either directory or File
        :return:
        """

        log_text = str()

        if keys in self.ts_dict:
            if self.ts_dict[keys] != mod_time:
                log_text = f"[+]{file_type}[+]:{keys}\tMODIFIED\tINFO:\nLast modified time: {self.ts_dict[keys]}\nModified hash: {self.return_hash(keys)}"
                self.ts_dict[keys] = mod_time
                self.hashes[keys] = self.return_hash(keys)
        else:
            self.ts_dict[keys] = mod_time
            log_text = f"[+]{file_type}[+]: {keys} CREATED\nINFO:\nCreation Time:{creation_time}\nHash: {self.return_hash(keys)}"
            self.hashes[keys] = self.return_hash(keys)

        if not self.is_first_run and log_text:
            self.logg.info(log_text)

    def return_hash(self, filename):
        """
        :return: Returns file/directory as dictionary object with key as file/dir name and value as hash.
        """
        while os.path.getsize(os.path.join(self.path, filename)) != 0:
            file_hash = hashlib.sha256()
            try:
                with open(os.path.join(self.path, filename), 'rb') as file:
                    for chunk in iter(lambda: file.read(4096), b""):
                        file_hash.update(chunk)
                        return file_hash.hexdigest()
            except PermissionError or FileNotFoundError:
                print(f"{filename} is empty or does not exist!")
                continue
        else:
            return f"No hash; File empty!"
