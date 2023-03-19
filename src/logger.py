import logging


class CustomFormatter(logging.Formatter):
    """
    Custom formatter for logging.
    """
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + log_fmt + reset,
        logging.INFO: grey + log_fmt + reset,
        logging.WARNING: yellow + log_fmt + reset,
        logging.ERROR: red + log_fmt + reset,
        logging.CRITICAL: bold_red + log_fmt + reset
    }

    def format(self, record):
        """
        Format the log message
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("ransomware")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)
