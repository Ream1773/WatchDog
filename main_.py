import os
import Logger
from WatchDog import WatchD


def main():
    """ ::Call logger, WatchDog class, User input:: """
    logg = Logger.get_logger()
    # prompt = input("Please enter the path you would like to monitor or 'exit':")
    prompt = r"C:\Users\Ream Sadan\Desktop\test"
    if prompt != "exit":
        os.chdir(prompt)
        passed_path = os.getcwd()
        init = WatchD(passed_path, logg, prompt)
        init.get_tree()
    else:
        exit()


if __name__ == "__main__":
    main()
