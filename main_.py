import os
import Logger
from WatchDog import WatchDog
# TODO:: Implement sys arg parser


def main():
    """ ::Call logger, WatchDog class, User input:: """
    logg = Logger.get_logger()
    # prompt = input("Please enter the path you would like to monitor or 'exit':")
    prompt = r"C:\Users\Ream Sadan\Desktop\test"
    if prompt != "exit":
        os.chdir(prompt)
        passed_path = os.getcwd()
        init = WatchDog(passed_path, logg)
        init.get_tree()
    else:
        exit(1)


if __name__ == "__main__":
    main()
