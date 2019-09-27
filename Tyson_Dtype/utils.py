import os

def get_data_file_list(data_dir, extension='.bin'):
  ''' 
  Get a sorted list of files in the given data directory that have
  a given extension.

  '''
  data_files = []
  for f in os.listdir(data_dir):
    if f.endswith(extension):
      data_files.append(os.path.join(data_dir,f))
  data_files.sort()
  return data_files
