import PIL.Image as Image
import imagemanipulator.util.fileutil as futil
import numpy as np

SUPPORTS_RGBA = {"png", "tiff", "tif", "webp", "bmp", "tga"}

def decode_image(image_path):
  image: Image.ImageFile = Image.open(image_path).convert("RGBA")
  pixel_data = np.array(image)

  return pixel_data

def encode_image(pixel_data, file_path):
  file_ext = futil.get_file_ext(file_path)
  has_alpha_channel = True

  if file_ext is None:
    # It's nearly impossible to reach this point
    # since the program checks the input and output file extension
    # the only way to get here is via a bug
    from imagemanipulator.logger import get_logger
    get_logger().error("The output file extension is empty...")

  if file_ext not in SUPPORTS_RGBA:
    pixel_data = pixel_data[..., :3]
    has_alpha_channel = False

  image = Image.fromarray(pixel_data).convert("RGBA" if has_alpha_channel else "RGB")
  image.save(file_path)