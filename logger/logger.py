import logging
from logger.colored_formatter import ColoredFormatter


def get_logger(file_name: str):

    # Create top level logger
    log = logging.getLogger()

    # Add console handler using our custom ColoredFormatter
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    cf = ColoredFormatter("[%(levelname)s]  %(message)s (%(filename)s:%(lineno)d)")
    ch.setFormatter(cf)
    log.addHandler(ch)

    # Add file handler
    fh = logging.FileHandler(file_name)
    fh.setLevel(logging.DEBUG)
    ff = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(ff)
    log.addHandler(fh)

    # Set log level
    log.setLevel(logging.DEBUG)
    return log
