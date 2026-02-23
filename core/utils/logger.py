# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import logging
import sys

from config.settings import get_settings

settings = get_settings()

def setup_logger(name: str = "Zirelia"):
    logger = logging.getLogger(name)
    
    if logger.hasHandlers():
        return logger

    # Set level based on env
    level = logging.DEBUG if settings.ENV == "development" else logging.INFO
    logger.setLevel(level)

    # Console Handler
    handler = logging.StreamHandler(sys.stdout)
    
    try:
        import colorlog
        handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            reset=True,
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
            }
        ))
    except ImportError:
        handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
    
    logger.addHandler(handler)
    
    # File Handler (Optional, for production)
    # file_handler = logging.FileHandler("Zirelia.log")
    # file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'))
    # logger.addHandler(file_handler)

    return logger

logger = setup_logger()
