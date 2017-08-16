import logging
import os
import errno

logfile = 'log/stat.log'

def mkdir_p(path):
    """http://stackoverflow.com/a/600612/190597 (tzot)"""
    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

class MakeFileHandler(logging.FileHandler):
    def __init__(self, logfile, mode='a', encoding=None, delay=0):
        mkdir_p(os.path.dirname(logfile))
        logging.FileHandler.__init__(self, logfile, mode, encoding, delay)


logger = logging.getLogger('stats')
logger.setLevel(logging.DEBUG)
fh = MakeFileHandler('log/stats.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('creating an instance of auxiliary_module.Auxiliary')
logger.info('created an instance of auxiliary_module.Auxiliary')
logger.info('calling auxiliary_module.Auxiliary.do_something')
logger.info('finished auxiliary_module.Auxiliary.do_something')
logger.info('calling auxiliary_module.some_function()')
logger.info('done with auxiliary_module.some_function()')


logger.error('done with auxiliary_module.some_function()')