try:
  from PIL import UnidentifiedImageError
  import numpy
  import scipy
except ImportError:
  print("Dependencies are not installed...\nPlease run \"pip install numpy pillow scipy\" to install dependencies...")

from argparse import ArgumentParser, ArgumentTypeError
from imagemanipulator.logger import get_logger
import imagemanipulator.exceptions as exceptions
from imagemanipulator.filters import get_filter
from imagemanipulator.parsers.syntaxparser import parse_syntax, parse_arguments
from imagemanipulator.imagedecoder import decode_image, encode_image
from imagemanipulator.util.fileutil import get_file_ext, is_file_ext_same
from PIL import UnidentifiedImageError
import os

def verify_file(file_name):
  if not os.path.exists(file_name):
    raise ArgumentTypeError("File does not exist...")
  return file_name

def create_parser():
  parser = ArgumentParser(description="A cli tool to manipulate images in various ways.")
  parser.add_argument("-f", "--filter", type=str, nargs="+", help="The filter to add.", required=True)
  parser.add_argument("-o", "--output", type=str, help="The path of the output file.", required=True)
  parser.add_argument("file_name", nargs=1, type=verify_file, help="The file to apply filters to...")
  return parser

def main():
  parser = create_parser()
  logger = get_logger()
  args, unknown_args = parser.parse_known_args()

  if len(unknown_args) > 0:
    logger.warning(f"Invalid arguments: {', '.join(map(lambda v: f"\"{v}\"", unknown_args))}")
    exit(1)

  output_file_name: str = args.output
  image_name: str = args.file_name[0]

  output_file_ext = get_file_ext(output_file_name)
  input_file_ext = get_file_ext(image_name)

  if (input_file_ext is None):
    logger.error("Input file has an extension that's not supported.")
  elif (not is_file_ext_same(input_file_ext, output_file_ext)):
    logger.error("Output file has a different extension than input file...")
  elif (output_file_ext is None):
    output_file_name += f".{input_file_ext}"

  try:
    pixel_data = decode_image(image_name)
    image_filters = ' '.join(args.filter)
    parsed_filters = parse_syntax(image_filters)
  except UnidentifiedImageError as e:
    logger.error(f"Input file is not an image file...")
  except exceptions.FilterNotFound as e:
    logger.error(e)
  except Exception as e:
    logger.debug(e)

  print("Applying filters...")

  try:
    for filter_name in parsed_filters:
      parsed_arguments = parse_arguments(filter_name, parsed_filters[filter_name])
      filter = get_filter(filter_name)

      pixel_data = filter.apply(pixel_data, parsed_arguments)
  except Exception as e:
    logger.error(e, exc_info=True)

  if os.path.exists(output_file_name):
    res = input(f"{output_file_name} already exists. Replace (y/n): ")
    if (res.lower() not in ['y', 'yes']):
      exit(0)
    os.remove(output_file_name)
  
  encode_image(pixel_data, output_file_name)


if __name__ == "__main__":
  main()