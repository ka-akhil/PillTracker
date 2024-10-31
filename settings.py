'''
App settings.

This module contains the settings for the PillTracker app.
'''

import ast
import os
from src.logger import logging

ENVS_READY = True

logging.info("Settings started")

if os.getenv('VIDEO'):
    VIDEO = os.getenv('VIDEO')
else:
    print('Path to video file not set.')
    ENVS_READY = False

logging.info("Settings completed")
