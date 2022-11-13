import os
import Logger
from WatchDog import WatchD
# CR: All magic numbers and text should be declared as constants here. For example:


def main():
    """ ::Call logger, WatchDog class, User input:: """
    logg = Logger.get_logger()
    # prompt = input("Please enter the path you would like to monitor or 'exit':")
    prompt = r"C:\Users\Ream\Desktop\test"
    if prompt != "exit":
        os.chdir(prompt)
        passed_path = os.getcwd()
        init = WatchD(passed_path, logg)
        init.get_tree()
    else:
        exit()


if __name__ == "__main__":
    main()
