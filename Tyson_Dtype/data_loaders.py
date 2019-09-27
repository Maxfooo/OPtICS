import os
import numpy as np

from utils import get_data_file_list
from OPtICS_dtypes import ioLoggedData_dtype
from OPtICS_dtypes import DataLoggedData_dtype
from OPtICS_dtypes import LoggerLoggedData_dtype
from OPtICS_dtypes import DataOut_dtype as lrads_dtype

def _calc_total_records(data_files):
  """ 
  Calculate the total number of data records in the list of data files.  
  NOTE: Uses lrads_dtype

  """
  total_records = int(0)
  for f in data_files:
    records = os.path.getsize(f) / lrads_dtype.itemsize
    total_records += int(records)
  return total_records


def load_data_iter(data_dir, dname='lrads', dtype=lrads_dtype):
  """ Generator based data loader. """
  data_files = get_data_file_list(data_dir)
  # Load the data 
  for f in data_files:
    data = np.fromfile(f, lrads_dtype)
    if dtype is lrads_dtype:
      yield data
    else:
      # Extract just the given data sub type
      yield data[dname]


def _load_data(data_dir, dname, dtype):
  """ The routine that loads data. Load LRADS data of a given dtype. """
  data_files = get_data_file_list(data_dir)
  total_records = _calc_total_records(data_files)
  # Pre-allocate an array of records so we don't have to cat
  # NOTE: May raise MemoryError if total records is large
  data = np.empty(total_records, dtype=dtype)
  # Load the data
  for n,f in enumerate(data_files):
    d = np.fromfile(f, lrads_dtype)
    start = n*len(d)
    stop = start + len(d)
    inds = range(start,stop)
    if dtype is lrads_dtype:
      data[inds] = d
    else:
      # Extract just the given sub data
      data[inds] = d[dname]
  return (data, len(data_files), total_records)


#
# Some helper routines for loading data
#
def load_data(data_dir):
  """ 
  Load all the data from a given data directory.  
  NOTE: This may be impossible due to the amount of data

  """
  return _load_data(data_dir, 'lrads', lrads_dtype)


def load_io_data(data_dir):
  """ Load all the IO task data from a given data directory """
  return _load_data(data_dir, 'io_data', ioLoggedData_dtype)


def load_data_data(data_dir):
  """ 
  Load all the Data task data from a given data directory
  NOTE: This may be impossible due to the amount of data

  """
  return _load_data(data_dir, 'data_data', DataLoggedData_dtype)


def load_logger_data(data_dir):
  """ Load all the Logger task data from a given data directory """
  return _load_data(data_dir, 'logger_data', LoggerLoggedData_dtype)

