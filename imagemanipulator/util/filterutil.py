import numpy as np

def _gaussian_equation(x, y, strength):
  s_2 = strength*strength
  k = 1/(2*np.pi*s_2) * np.exp(-(x**2+y**2)/(2*s_2))

  return k

def _identity_gaussian_kernel(kernel_size):
  identity_kernel = np.zeros((kernel_size, kernel_size))
  k_2 = kernel_size//2

  identity_kernel[k_2, k_2] = 1
  return identity_kernel

def create_gaussian_kernel(kernel_size, strength):
  gaussian_kernel = np.zeros((kernel_size, kernel_size))
  m = kernel_size//2

  offset = np.arange(-m, m+1)
  x, y = np.meshgrid(offset, offset)

  gaussian_kernel = _gaussian_equation(x, y, strength)
  
  if kernel_size < 1e-10:
    return _identity_gaussian_kernel(kernel_size)

  gaussian_kernel /= gaussian_kernel.sum()
  return gaussian_kernel