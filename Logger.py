import logging
from main import WatchD, run


def logger():
    logging.basicConfig(filename='Watcher.log', level=logging.INFO, encoding='utf-8',
                        format='%(asctime)s:%(levelname)s:')
    init = WatchD(run())
    logging.info(init.get_tree())


logger()
