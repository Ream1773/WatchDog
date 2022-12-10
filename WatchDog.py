import logging
import os
import hashlib
# TODO:: Implement the hasher function to make the program more genuine.
# TODO:: Add feature that shows if the directory is empty?


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
        self.hash_dict = dict()
        self.info_ = Info(path)

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
        old_hashes = dict()

        for root, dirs, files in os.walk(self.path):
            walk_files.update({os.path.join(root, name): 'Directory' for name in dirs})
            walk_files.update({os.path.join(root, name): 'File' for name in files})
            old_hashes.update({os.path.join(root, name): self.info_.return_hash(walk_files) for name in files})
        # self.hash_dict[files] = old_hashes.values()
        self._check_existence(walk_files, old_hashes)

    def _check_existence(self, walk_files: dict, old_hashes: dict):

        """
        * Checks if item exists:
        * Checks if item is a file or directory.
        * Creates modification time if item exists.
        """

        self.hash_dict = self.info_.return_hash(walk_files)

        for file in list(self.ts_dict.keys()):
            if file not in walk_files.keys():
                self.logg.info(f"{self.info_.return_type().values()}[-] {file} deleted!")   # TODO:: Fix the dict.values appearing instead of file type
                self.ts_dict.pop(file, None)

        for file in list(self.hash_dict.keys()):
            if file not in old_hashes.keys():
                self.logg.info(f"[-]{self.info_.return_type()}[-]{file} deleted!")
                self.hash_dict.pop(file, None)

        for keys, file_type in walk_files.items():
            try:
                stat = os.stat(keys)
            except FileNotFoundError:
                self.ts_dict.pop(keys, None)
                self.hash_dict.pop(keys, None)  # *TEST*
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

        hash_list = [item for item in self.hash_dict.values()]
        next_hash = iter(hash_list)

        log_text = str()

        # TODO:: Check if mod time is different and if hash is also diff, if hash not different then file hasn't been modified,
        # TODO:: if it has then previous hash is replace with new hash

        if keys in self.ts_dict:
            if self.ts_dict[keys] != mod_time and self.hash_dict[keys] != hash_list:
                log_text = f"[+]{file_type}[+]:{keys}\tMODIFIED\tINFO:\nLast Modified time: {self.ts_dict[keys]}\nHash: {self.hash_dict[keys]}\t Hash modified!"
                self.ts_dict[keys] = mod_time
                self.hash_dict[keys] = hash_list
        else:
            self.ts_dict[keys] = mod_time
            self.hash_dict[keys] = hash_list
            log_text = f"[+]{file_type}[+]: {keys} added!\nINFO:\nCreation Time:{creation_time}\nHash: {self.hash_dict.values()}"

        if not self.is_first_run and log_text:
            self.logg.info(log_text)

    # TODO:: -> Check if mod time is different and if hash is also diff, if hash not diff then file hasn't been modified,
    # TODO:: if it has then previous hash is replace with new hash
    # def _hash_comparer(self, prev_hash, mod_time):
    #     if len(prev_hash) != len(new_hash):
    #         return False
    #     for i in range(len(prev_hash)):
    #         if prev_hash[i] != new_hash[i]:
    #             return False
    #     return True

    # def _hash_comparer(self, prev_hash, new_hash):
    #     if len(prev_hash) != len(new_hash):
    #         return False
    #     for i in range(len(prev_hash)):
    #         if prev_hash[i] != new_hash[i]:
    #             return False
    #     return True

class Info:

    """
    Info class that collects all relevant
    information on the items in the given path.
    """

    def __init__(self, path):
        self.entity_info = dict()
        self.hashes = dict()
        self.path = path

    def return_type(self):

        """
        Necessary if first run does not have items in path.
        :return: Returns if item is File or Directory.
        """

        for root, dirs, files in os.walk(self.path):
            self.entity_info.update({os.path.join(root, name): 'Directory' for name in dirs})
            self.entity_info.update({os.path.join(root, name): 'File' for name in files})
            return self.entity_info

    def return_hash(self, walk_files: dict):

        """
        :return: Returns file/directory as dictionary object with key as file/dir name and value as hash.
        """

        for filename in list(walk_files.keys()):
            if filename not in list(walk_files.keys()):
                self.hashes.pop(filename, None)
                continue
            try:
                if os.path.getsize(os.path.join(self.path, filename)) == 0:
                    continue
                file_hash = hashlib.sha256()
                with open(os.path.join(self.path, filename), 'rb') as file:
                    for chunk in iter(lambda: file.read(4096), b""):
                        file_hash.update(chunk)
                        self.hashes[filename] = file_hash.hexdigest()
            except PermissionError or FileNotFoundError as e:
                self.hashes.pop(filename, None)
                print(f"{filename} is empty or does not exist!")
                continue
        return self.hashes
