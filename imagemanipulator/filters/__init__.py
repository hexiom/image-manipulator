from .arguments import Argument
import imagemanipulator.filters.filter_methods as fmethods
import imagemanipulator.logger as imlogger

class Filter:
  def __init__(self, callback, valid_args:list[Argument]=[]) -> None:
    logger = imlogger.get_logger()
    # Sort optional arguments at the end...
    self.callback = callback
    self.args = valid_args

    in_optional_args = False
    argument_names = set()
    
    for argument in valid_args:
      if (argument.optional_value):
        in_optional_args = True
      elif (in_optional_args and argument.optional_value is None):
        logger.critical("A filter has a required value after an optional value, please fix it...")
      elif (argument.name in argument_names):
        logger.critical(f"A filter has two arguments with same name (\"{argument.name}\")")

      argument_names.add(argument.name)

  def parse_arguments(self, filter_name: str, arguments: list[str]):
    from logger import get_logger
    from imagemanipulator.parsers.syntaxparser import parse_arguments

    try:
      return parse_arguments(filter_name, self, arguments)
    except Exception as e:
      logger = get_logger()
      logger.error(e)
    
  def get_required_args(self):
    return filter(lambda arg: not arg.optional, self.args)

  def apply(self, pixel_data, arguments):
    return self.callback(pixel_data, arguments)

_FILTERS = {
  'crop': Filter(fmethods.crop, [
                    Argument("crop_width", Argument.INT),
                    Argument("crop_height", Argument.INT),
                    Argument("centre_x", Argument.INT, Argument.Allow.allow_positive, optional_value=-1), 
                    Argument("centre_y", Argument.INT, Argument.Allow.allow_positive, optional_value=-1),
                ]),
  'rotate': Filter(fmethods.rotate, [Argument("n", Argument.INT)]),
  'blur': Filter(fmethods.gaussian_blur, [Argument("strength", Argument.NUMBER, lambda value: value > 0,  optional_value=6)]),
  'flip': Filter(fmethods.flip, [Argument("direction", Argument.STRING, Argument.Allow.case_insensitive_from_list(['x', 'y', 'xy', 'yx']))]),
  'greyscale': Filter(fmethods.greyscale, []),
  'tint': Filter(fmethods.tint, [
                    Argument("r", Argument.INT, Argument.Allow.is_color), 
                    Argument("g", Argument.INT, Argument.Allow.is_color), 
                    Argument("b", Argument.INT, Argument.Allow.is_color), 
                    Argument("strength", Argument.PERCENTAGE, Argument.Allow.is_between_inclusive(0, 1), optional_value=0.1)
                ])
}

def is_valid_filter(name: str):
  return name in _FILTERS.keys()

def get_filter(name: str):
  return _FILTERS[name]