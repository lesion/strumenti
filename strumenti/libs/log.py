"""Logging functions"""

import logging

# Setup the logger
logging.basicConfig(
  level=logging.WARNING,
  #format="[%(levelname)-8s] %(asctime)s %(module)s:%(lineno)d %(message)s",
  format="[%(levelname)-8s] %(message)s",
  datefmt="%H:%M:%S"
)


def setLoggerLevel( level ):
  """Sets the logger level.

    @param level string, desired level of logging
    could be one of:
    * debug
    * info
    * warning
    * error
    * none
  """

  levels = {
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "none": logging.CRITICAL,
    "debug": logging.DEBUG
  }

  if level not in levels:
    return

  global log
  log.setLevel(levels[level])

# Get the logger
log   = logging.getLogger()
info  = log.info
warn  = log.warn
err   = log.error
debug = log.debug
fatal = log.fatal
