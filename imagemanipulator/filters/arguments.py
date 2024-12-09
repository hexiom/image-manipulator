from imagemanipulator.logger import get_logger
from imagemanipulator.exceptions import ArgumentTypeNotFound, ValueNotAllowedException

def _parse_percentage(value: str):
  if value.endswith("%"):
    n = float(value[:-1])

    return n / 100
  
  return float(value)

def _is_truthy(value: str):
  truthy = set(['y', 'yes', '1', 't', 'true'])
  return (value.lower() in truthy)

def _check_predicates(value, *args):
  for predicate in args:
    if not predicate(value):
      return False
    
  return True

class ArgumentAllowMethods:
  @staticmethod
  def is_color(value: int):
    return value >= 0 and value <= 255
  
  @staticmethod
  def is_between_inclusive(min, max):
    return lambda value: value >= min and value <= max
  
  def allow_positive(value):
    return value > 0
  
  def allow_negative(value):
    return value < 0
  
  def case_insensitive_from_list(l: list[str]):
    return lambda value: value.lower() in l
  
  def not_from_list(l: list[any]):
    return lambda value: value not in l

  def combine_predicates(*args):
    return lambda value: _check_predicates(value, *args)

class Argument:
  INT = 'int'
  NUMBER = 'number'
  STRING = 'string'
  BOOL = 'bool'
  PERCENTAGE = 'percentage'
  Allow = ArgumentAllowMethods

  def __init__(self, name: str, type: str, allow=None, optional_value=None) -> None:
    self.name = name
    self.type = type
    self.optional_value = optional_value

    if (allow is None):
      self.allow = lambda x: True
    else:
      self.allow = allow

  def parse(self, value: str):
    logger = get_logger()
    parsed_value = None

    try:
      match (self.type):
        case Argument.INT:
          parsed_value = int(value)
        
        case Argument.NUMBER:
          parsed_value = float(value)
        
        case Argument.BOOL:
          # Using a custom truthy check since bool() returns true for any
          # string value, which I don't personally like, but it makes sense.
          parsed_value = _is_truthy(value)

        case Argument.PERCENTAGE:
          parsed_value = _parse_percentage(value)
          
        case Argument.STRING:
          # No support for single/double quotes with spaces
          # There should be no need for them anyways in most cases
          parsed_value = value
        
        case _:
          raise ArgumentTypeNotFound(self.type)
      
      if (not self.allow(parsed_value)):
        raise ValueNotAllowedException(self, value)

      return parsed_value
    except ArgumentTypeNotFound as e:
      logger.critical(e)