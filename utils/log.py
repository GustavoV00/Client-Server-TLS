"""
    Module that contains logging utilities
"""

import logging
import sys

class Error(Exception):
    """
        Error handler for the logging module
    """


class MissingSetup(Error):
    """
        If the logging setup was forgotten
    """



class Logging(object):
    """
        Class to hold with logging operations
    """
    _root_logger = None
    LOG_FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 

    @classmethod
    def clear_root_logger(cls):
        """
            Reset _root_logger to default
        """
        cls._root_logger = None


    @classmethod
    def setup(cls, stdout_log=False, logger_file_path=None, logger_level=logging.WARNING):
        """
            Setup the logging

            :param bool stdout_log: If we should log to stdout or not
            :param str logger_file_path: The file path to where the log file will be stored
            :param int logger_level: The log level to use (based on log levels from logging module)
        """

        if not cls._root_logger:
            cls._root_logger = logging.getLogger()
            cls._root_logger.setLevel(logger_level)
            if stdout_log:
                stdout_handler = logging.StreamHandler(sys.stdout)
                stdout_handler.setLevel(logger_level)
                stdout_handler.setFormatter(logging.Formatter(Logging.LOG_FORMATTER))
                cls._root_logger.addHandler(stdout_handler)
            if logger_file_path:
                fh = logging.FileHandler(logger_file_path)
                fh.setLevel(logger_level)
                fh.setFormatter(logging.Formatter(Logging.LOG_FORMATTER))
                cls._root_logger.addHandler(fh)


    @classmethod
    def get_logger(cls, logger_name='default'):
        """
            Get a logger instance
            :param str logger_name: The logger name to use
            :return: A logger instance
            :raises: MissingSetup - if setup was not performed
        """
        if not cls._root_logger:
            raise MissingSetup("Missing setup root logger")
        return logging.getLogger(logger_name)