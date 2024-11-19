import logging
import os
import traceback

class Logger:
    def __init__(self, log_directory='app/logs', log_filename='app.log'):
        self.logger = self.__set_logger(log_directory, log_filename)

    def __set_logger(self, log_directory, log_filename):
        os.makedirs(log_directory, exist_ok=True)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        log_path = os.path.join(log_directory, log_filename)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)

        if logger.hasHandlers():
            logger.handlers.clear()

        logger.addHandler(file_handler)
        return logger

    def add_to_log(self, level: str, message: str):
        try:
            log_method = getattr(self.logger, level, None)
            if log_method:
                log_method(message)
            else:
                self.logger.error(f"Invalid log level: {level}")
        except Exception as ex:
            self.logger.error(f"Error while logging message: {message} - Exception: {str(ex)}")
            print(traceback.format_exc())
