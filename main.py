import os


class WatchD:
    def __init__(self, path):
        self.path = path
        self.og_file_stamp = 0
        self.og_dir_stamp = 0

    def get_tree(self):
        while True:
            for root, dirs, files in os.walk(self.path, topdown=True):
                for name in files:
                    file_key = os.path.join(root, name)
                    file_stamp = os.stat(file_key).st_mtime
                    # print(file_key + "::", file_stamp)
                    if file_stamp != self.og_file_stamp:
                        print("{0} was modified at {1}".format(file_key, file_stamp))
                        self.og_file_stamp = file_stamp
                    else:
                        return
                for name in dirs:
                    dir_key = os.path.join(root, name)
                    dir_stamp = os.stat(dir_key).st_mtime
                    if dir_stamp != self.og_dir_stamp:
                        print("{0} was modified at {1}".format(dir_key, dir_stamp))
                        self.og_dir_stamp = dir_stamp
                        return
                    else:
                        return

    # def handler(self, og_dir_stamp, og_file_stamp):


run = WatchD(r"C:\Users\user\Desktop\stam")
run.get_tree()
