import logging
import os

# TODO:: Implement the hasher function to make the program more genuine.
# TODO:: Add feature that shows if the directory is empty.
# TODO:: Fix bug that doesn't show file deletions if all files in the directory are deleted.


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
        Calls the _get_timestamps class method that which then scans all the
        elements of the given path param.
        :return: -> None
        """
        for root, dirs, files in os.walk(self.path):
            self._check_existence(root, files, False)
            self._check_existence(root, dirs, True)

    def _check_existence(self, root, walk_files, is_dir):
        """
        * Checks if entity is a file or directory.
        * Checks if the file/dir exists and creates modification time if file/dir exists.
        :param -> root: Path provided by main.py essentially
        :param -> walk_files: iteration of all files in provided path.
        :param -> is_dir: function to check file type(dir/file)
        :return: -> None
        """
        if is_dir:
            file_type = "Directory"
        else:
            file_type = "File"

        for name in walk_files:
            keys = os.path.join(root, name)
            try:
                stat = os.stat(keys)
            except FileNotFoundError:
                self.entities.pop(keys, None)
                self.logg.info(f"[-]: {file_type} [-] {keys} deleted!")
                continue

            mod_time = stat.st_mtime
            creation_time = stat.st_ctime
            self.check_changed(keys, mod_time, creation_time, file_type)

    def check_changed(self, keys, mod_time, creation_time, file_type):
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
