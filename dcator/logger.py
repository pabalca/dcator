import logging
import types


def log_separator(self, size=70):
    self.handler.setFormatter(self.blank_formatter)
    self.info(size*'-')
    self.handler.setFormatter(self.formatter)


def log_logo(self):
    self.handler.setFormatter(self.blank_formatter)
    self.info(69 * '-' + "|")
    logo = """                                      
  _              _              
 | |            | |             
 | | ___ __ __ _| | _____ _ __  
 | |/ / '__/ _` | |/ / _ \ '_ \ 
 |   <| | | (_| |   <  __/ | | |
 |_|\_\_|  \__,_|_|\_\___|_| |_|
    """
    self.info(logo)
    self.separator()
    self.handler.setFormatter(self.formatter)


def create_logger():
    # Create a handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(fmt=" > %(message)s")
    formatter = logging.Formatter(fmt=" %(message)-65s")
    blank_formatter = logging.Formatter(fmt="")
    handler.setFormatter(formatter)

    # Create a logger, with the previously-defined handler
    logger = logging.getLogger("kraken")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    # Save some data and add a method to logger object
    logger.handler = handler
    logger.formatter = formatter
    logger.blank_formatter = blank_formatter
    logger.separator = types.MethodType(log_separator, logger)
    logger.logo = types.MethodType(log_logo, logger)

    return logger


logger = create_logger()
