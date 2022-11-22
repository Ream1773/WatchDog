import os
# TODO:: Implement the hasher function to make the program more genuine.
# TODO:: Fix exception that occasionally occurs when files/dirs are deleted.


class WatchDog:
    """
    Main class that scans files recursively of provided path
    and logs changes made to them.
    """
    def __init__(self, path: str, logg):
        self.path = path
        self.logg = logg
        self.is_first_run = True
        self.entities = {}

    def get_tree(self):
        if self.is_first_run:
            self.entities.clear()
        while True:
            self._get_entities(self.path)
            self.is_first_run = False

    def _get_entities(self, path: str):
        """
        Calls the _get_timestamps class method that which then scans all the
        elements of the given path param.
        :param path:
        :return: None
        """
        for root, dirs, files in os.walk(path):
            self._check_existence(root, files, False)
            self._check_existence(root, dirs, True)

    def _check_existence(self, root, walk_files, is_dir):
        """
        * Checks if entity is a file or directory.
        * Checks if the file/dir exists and sets modification time if file/dir exists.
        :param -> root:
        :param -> walk_files:
        :param -> is_dir:
        :return: -> None
        """
        if is_dir:
            file_type = "Directory"
        else:
            file_type = "File"

        for name in walk_files:
            keys = os.path.join(root, name)
            try:
                if not os.path.exists(keys):
                    self.entities.pop(name, None)
                    self.logg.info(f"[-]: {file_type} [-] {keys} deleted!")
                else:
                    mod_time = os.stat(keys).st_mtime
                    creation_time = os.stat(keys).st_ctime
                    self.check_changed(keys, mod_time, creation_time, file_type)
            except FileNotFoundError as e:
                print(f"{e}")
                pass

    def check_changed(self, keys, mod_time, creation_time, file_type):
        log_text = str()

        if keys in self.entities:
            if self.entities[keys] != mod_time:
                log_text = f"[+] {file_type} [+]: {keys} modified at {self.entities[keys]}!"
                self.entities[keys] = mod_time
        else:
            self.entities[keys] = mod_time
            log_text = f"[+]NEW {file_type} [+]: {keys} added at {creation_time}!"
            if not os.path.exists(keys):
                self.entities.pop(keys, None)

        if not self.is_first_run and log_text:
            self.logg.info(log_text)
