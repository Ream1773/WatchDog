import logging


def get_logger():
    """
    ::Define logger function for main WatchD class::
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler('Watcher.log')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

# def test1():
    # test = WatchD()
    # print(test.get_tree(r"C:\Users\Ream Sadan\Desktop\test"))
    # get_logs(test.get_tree(r"C:\Users\Ream Sadan\Desktop\test"))
