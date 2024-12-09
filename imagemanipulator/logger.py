import logging, sys

_LOGGING_COLORS = {
  'DEBUG': '\033[32m',
  'INFO': '\033[34m',
  'WARNING': '\033[33m',
  'ERROR': '\033[31m',
  'CRITICAL': '\033[1;31m'
}

_DEFAULT_COLOR = '\033[0m'
_LOGGING_LEVEL_FORMAT = "[%s]:"

_IS_DEBUG = True
_singleton = None

class CustomStreamHandler(logging.StreamHandler):
  def emit(self, record: logging.LogRecord) -> None:
    if record.levelno == logging.DEBUG and not _IS_DEBUG:
      return
    
    super().emit(record)

    if record.levelno >= logging.ERROR:
      sys.exit(1)

class CustomColorFormatter(logging.Formatter):
  def format(self, logrecord: logging.LogRecord):
    levelname = logrecord.levelname
    color = _LOGGING_COLORS.get(levelname, '')
    message = super().format(logrecord)
    level_format_colored = f"{color}{_LOGGING_LEVEL_FORMAT % levelname} "
    display_message = f"{level_format_colored}{_DEFAULT_COLOR}{message}"

    if levelname == "CRITICAL":
      display_message = f"{level_format_colored}{message}{_DEFAULT_COLOR}"
    
    return display_message

def _create_logger():
  logger = logging.getLogger("image_manipulator")
  console_stream = CustomStreamHandler()
  formatter = CustomColorFormatter('%(message)s')

  console_stream.setFormatter(formatter)

  logger.addHandler(console_stream)
  logger.setLevel(logging.DEBUG)

  return logger

def get_logger():
  global _singleton

  if not _singleton:
    logger = _create_logger()
    _singleton = logger
  
  return _singleton