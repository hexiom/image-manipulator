import PIL.ImageColor
import numpy as np
import imagemanipulator.util.filterutil as util
from imagemanipulator.logger import get_logger
import imagemanipulator.exceptions as exceptions
from scipy.signal import convolve2d

def gaussian_blur(pixel_data, args):
  kernel_size = 5
  strength = args["strength"]
  gaussian_kernel = util.create_gaussian_kernel(kernel_size, strength)
  result = pixel_data

  for channel in range(4):
    result[..., channel] = convolve2d(pixel_data[..., channel], gaussian_kernel, mode='same', boundary='symm')

  return pixel_data

def crop(pixel_data, args):
  image_width, image_height = pixel_data.shape[:2]
  cx = args["centre_x"]
  cy = args["centre_y"]

  if cx < 0:
    cx = image_width//2
  
  if cy < 0:
    cy = image_height//2

  crop_width, crop_height = args["crop_width"], args["crop_height"]
  w_offset, h_offset = crop_width//2, crop_height//2
  rect_left, rect_right = cx-w_offset, cx+w_offset
  rect_top, rect_bottom = cy-h_offset, cy+h_offset

  if (rect_left < 0 or rect_right > image_width-1 or rect_top < 0 or rect_bottom > image_height-1):
    raise exceptions.FilterFailedToApplyException("Crop", "Crop dimensions are outside valid bounds...")
  
  return pixel_data[rect_top:rect_bottom, rect_left:rect_right]
  
def flip(pixel_data, args):
  flip_dir = args["direction"].lower()
  flip_x = 'x' in flip_dir
  flip_y = 'y' in flip_dir

  flipped_pixel_data = pixel_data

  if flip_x:
    flipped_pixel_data = np.fliplr(flipped_pixel_data)

  if flip_y:
    flipped_pixel_data = np.flipud(flipped_pixel_data)

  return flipped_pixel_data

def rotate(pixel_data, args):
  return np.rot90(pixel_data, -args["n"])

def greyscale(pixel_data, _):
  greyscale_weights = np.array([0.299, 0.587, 0.114]) # Magic values...
  height, width = pixel_data.shape[:2]

  for y in range(height):
    for x in range(width):
      color = pixel_data[y, x, :3]
      grey = color @ greyscale_weights

      pixel_data[y, x, :3] = grey

  return pixel_data

def tint(pixel_data, args):
  tint_color = np.array([[args["r"], args["g"], args["b"]]])
  strength = args["strength"]
  color = pixel_data[..., :3]

  pixel_data[..., :3] = (color * (1-strength) + tint_color * strength)
  return pixel_data

def tone_map(pixel_data, args):
  pass