import os
import Logger
# from . import hash_gen


""" ::Call logger:: """
logg = Logger.get_logger()


class WatchD:
    """
    Main class that scans files recursively of provided path
    and logs changes made to them.
    """
    def __init__(self):
        self.file_ts = {}
        self.dir_ts = {}

    def get_tree(self, path: str):
        while True:
            for root, dirs, files in os.walk(path, topdown=True):
                for name in files:
                    file_keys = os.path.join(root, name)
                    file_stamps = os.stat(file_keys).st_mtime
                    if file_keys in self.file_ts:
                        if self.file_ts[file_keys] != file_stamps:
                            print("Changed")
                            self.file_ts[file_keys] = file_stamps
                    else:
                        self.file_ts[file_keys] = file_stamps
                        logg.info(f"New file {file_keys} added!")
                    # TODO:: make sure to remove files upon deletion to prevent crashes
                    # TODO:: implement same feature for directories
                for name in dirs:
                    dir_keys = os.path.join(root, name)
                    dir_stamps = os.stat(dir_keys).st_mtime
                    self.dir_ts[dir_keys] = dir_stamps
                    return self.dir_ts, self.file_ts
                    # logg.info("{0} was modified at {1}".format(dir_key, dir_stamp))

    def get_info(self):
        print(self.file_ts)
        print(self.dir_ts)


def run():
    while True:
        try:
            # prompt = input("Please enter the path you would like to monitor or 'exit':")
            prompt = r"C:\Users\Ream Sadan\Desktop\test"
            if prompt != "exit":
                os.chdir(prompt)
                passed_path = os.getcwd()
                init = WatchD()
                init.get_tree(passed_path)
                init.get_info()
            else:
                break
        except KeyboardInterrupt and FileNotFoundError as err:
            print(err)
            exit(1)


if __name__ == "__main__":
    run()
