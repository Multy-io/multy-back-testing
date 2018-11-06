import os
import logging
from time import strftime

LOG_DIR_NAME = 'logs'
log_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', LOG_DIR_NAME))
log_path = os.path.join(log_dir_path, f'launch_{strftime("%Y-%m-%d")}.log')

logger = logging.getLogger('Common Logger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(log_path)
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
