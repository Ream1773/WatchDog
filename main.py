import os
import Logger

""" ::Call logger:: """
logg = Logger.get_logger()


class WatchD:
    """
    Main class that scans files recursively of provided path
    and logs changes made to them.
    """
    def __init__(self):
        self.og_file_stamp = int()
        self.og_dir_stamp = int()

    def get_tree(self, path: str):
        while True:
            for root, dirs, files in os.walk(path, topdown=True):
                for name in files:
                    file_key = os.path.join(root, name)
                    file_stamp = os.stat(file_key).st_mtime
                    self.og_file_stamp = file_stamp
                    # print(self.og_file_stamp, file_stamp)
                    if self.og_file_stamp != file_stamp:
                        self.og_file_stamp = file_stamp
                        logg.info("{0} was modified at {1}".format(file_key, file_stamp))
                for name in dirs:
                    dir_key = os.path.join(root, name)
                    dir_stamp = os.stat(dir_key).st_mtime
                    self.og_dir_stamp = dir_stamp
                    # print(self.og_dir_stamp, dir_stamp)
                    if self.og_dir_stamp != dir_stamp:
                        self.og_dir_stamp = dir_stamp
                        logg.info("{0} was modified at {1}".format(dir_key, dir_stamp))


def run():
    while True:
        try:
            prompt = input("Please enter the path you would like to monitor or 'exit':")
            if prompt != "exit":
                os.chdir(prompt)
                passed_path = os.getcwd()
                init = WatchD()
                init.get_tree(passed_path)
            else:
                break
        except KeyboardInterrupt and FileNotFoundError as err:
            print(err)
            exit(1)


if __name__ == "__main__":
    run()
