FILE_EXTENSION_ALIASES = {'jpeg': 'jpeg'}

def get_file_ext(file_name):
  dot_split = file_name.split(".")

  if (len(dot_split) == 0):
    return None
  
  return dot_split[-1]

def is_file_ext_same(ext1: str, ext2: str):
  if ext1 in FILE_EXTENSION_ALIASES:
    ext1 = FILE_EXTENSION_ALIASES[ext1]

  if ext2 in FILE_EXTENSION_ALIASES:
    ext2 = FILE_EXTENSION_ALIASES[ext2]

  return ext1 == ext2