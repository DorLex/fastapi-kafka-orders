import logging

formatter = logging.Formatter(
    '%(levelname)s (%(asctime)s) %(name)s: %(message)s (file: %(filename)s, func: %(funcName)s, line: %(lineno)d)'
)
