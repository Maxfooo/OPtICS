#!/bin/python

from data_loaders   import load_data_iter
from .OPtICS_dtypes import ioLoggedData_dtype as io_dtype
from .OPtICS_dtypes import DataLoggedData_dtype as data_dtype
from .OPtICS_dtypes import LoggerLoggedData_dtype as logger_dtype
from .OPtICS_dtypes import DataOut_dtype as lrads_dtype

def print_usage():
  print('Usage: test_load_data <data dir> <data type>')
  print('Supported types: ')
  print('  lrads = All the data')
  print('     io = IO task data only')
  print('   data = Data task data only')
  print('    log = Logger task data only')


def main():
    data_dir = "/home/maxr/Desktop/PYTHON_Workspace/lrads_ex_data/"
    data_type = 'lrads'

    if data_type == 'lrads':
        dtype = lrads_dtype
    elif data_type == 'io':
        dtype = io_dtype
    elif data_type == 'data':
        dtype = data_dtype
    elif data_type == 'log':
        dtype = logger_dtype
    else:
        print('Error: Unknown data type')
        return -1

    datas = load_data_iter(data_dir, data_type, dtype)

    for n,data in enumerate(datas):
        print('data %d with %d records' % (n, data.shape[0]))

if __name__ == "__main__":
	main()
