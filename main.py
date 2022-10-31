import os


class WatchD(path=None):
    def __init__(self):
        self.path = str()

    def get_path(self, path=None):
        while True:
            if path is None:
                print(f"Path cannot be empty!")
            else:
                print(path)
                return path

    def get_tree(self, path):
        epochs = {}
        epochs_ = {}
        for root, dirs, files in os.walk(path, topdown=True):
            for name in files:
                # print(os.path.join(root, name))
                key = os.path.join(root, name)
                try:
                    for item in name:
                        epochs[key] = os.path.getmtime(root)
                    print(epochs)
                except TypeError as e:
                    print(e)
            for name in dirs:
                print(os.path.join(root, name))
                # # DN = os.path.join(root, name)#Dir Name
                # TOM = os.path.getmtime(root) # Time Of Modification
                # try:
                #     for items in dirs:
                #         epochs_[os.path.join(root, name)] = epochs_[str(TOM)]
                # except TypeError as err:
                #     print(err)
                # print(os.path.getmtime(root))

    # def get_create(self):
    #     print(os.path.getmtime())


run = WatchD()
run.get_tree(r"C:\Users\Ream\Desktop\NEW")
