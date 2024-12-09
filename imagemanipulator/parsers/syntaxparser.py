import re
import imagemanipulator.logger as imlogger
import imagemanipulator.filters as imfilter
import imagemanipulator.exceptions as exceptions

# Parses syntax for filters that resembles method calls.
# "filters" is a string of filters to add seperated by commas
# All whitespace in "filters" will be removed.
def parse_syntax(filters: str):
  filters = re.sub(r"\s+", "", filters)
  matches = re.findall(r"(\w+)\((.*?)\)", filters)
  filter_array = {}

  for match in matches:
    filter_name, arguments = match

    if not imfilter.is_valid_filter(filter_name):
      raise exceptions.FilterNotFound(filter_name)
    
    arguments = filter(lambda v: len(v) > 0, arguments.split(","))
    filter_array[filter_name] = list(arguments)

  return filter_array

# Parses arguments that may be inside of a filter call
# For example, "args" may be ["1", "2", "90", "abc", "n=4"]
# Throws an ArgumentSyntaxError for invalid syntax and an IndexError for out of range parameters
def parse_arguments(filter_name: str, args: list[str]):
  image_filter = imfilter.get_filter(filter_name)
  logger = imlogger.get_logger()
  parsed_arguments = {}
  only_keyword_arguments = False

  for i, arg in enumerate(args):
    keyword_arguments = re.match(r'^([^\s=]+)=([^\s=]+)$', arg)

    if (not keyword_arguments):
      if (only_keyword_arguments):
        raise exceptions.ArgumentSyntaxError(f"Cannot have positionals after keyword arguments for filter \"{filter_name}\"")

      if (i >= len(image_filter.args)):
        raise IndexError(f"Argument index out of range for filter \"{filter_name}\"")
      
      argument = image_filter.args[i]
      parsed_arguments[argument.name] = argument.parse(arg)
    else:
      key, value = keyword_arguments.groups()
      arg_def = next((arg for arg in image_filter.args if arg.name == key), None)

      if (arg_def is None):
        logger.error(f"Argument \"{key}\" doesn't exists for filter \"{filter_name}\"")

      parsed_arguments[key] = arg_def.parse(value)
      only_keyword_arguments = True
    
  for arg in image_filter.args:
    if not arg.name in parsed_arguments:
      if arg.optional_value is None:
        raise exceptions.RequiredValueNotFound(arg, filter_name)
      
      parsed_arguments[arg.name] = arg.optional_value
    
  return parsed_arguments