class ArgumentSyntaxError(Exception):
  def __init__(self, message: str) -> None:

    super().__init__(message)

class ArgumentTypeNotFound(Exception):
  def __init__(self, type: str) -> None:
    super().__init__(f"Argument type \"{type}\" not found. Please use a valid argument type for filters.")

class FilterNotFound(Exception):
  def __init__(self, filter_name: str) -> None:
    super().__init__(f"Filter \"{filter_name}\" not found.")

class RequiredValueNotFound(Exception):
  def __init__(self, arg, filter_name) -> None:
    super().__init__(f"Required argument \"{arg.name}\" ({arg.type}) is empty for filter \"{filter_name}\"...")

class ValueNotAllowedException(Exception):
  def __init__(self, argument, arg_value) -> None:
    super().__init__(f"\"{arg_value}\" is not a valid value for \"{argument.name}\" ({argument.type}).")

class FilterFailedToApplyException(Exception):
  def __init__(self, filter_name: str, message: str):
    super().__init__(f"[{filter_name}]: {message}")