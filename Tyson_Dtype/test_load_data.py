##!/bin/python
#
#import sys
#
#from lrads_ppp_us.data_loaders import load_data
#from lrads_ppp_us.data_loaders import load_io_data
#from lrads_ppp_us.data_loaders import load_data_data
#from lrads_ppp_us.data_loaders import load_logger_data
#
#def print_usage():
#  print('Usage: test_load_data <data dir> <data type>')
#  print('Supported types: ')
#  print('  lrads = All the data')
#  print('     io = IO task data only')
#  print('   data = Data task data only')
#  print('    log = Logger task data only')
#
#
#def main():
#  if len(sys.argv) < 2:
#    print('Error: No data directory or type given')
#    print_usage()
#    return -1
#
#  data_dir = sys.argv[1]
#
#  if len(sys.argv) < 3:
#    data_type = 'lrads'
#  else:
#    data_type = sys.argv[2]
#
#  print('Loading %s data' % data_type)
#
#  if data_type == 'lrads':
#    loader = load_data
#  elif data_type == 'io':
#    loader = load_io_data
#  elif data_type == 'data':
#    loader = load_data_data
#  elif data_type == 'log':
#    loader = load_logger_data
#  else:
#    print('Error: Unknown data type')
#    return -1
#
#  data, num_files, num_records = loader(data_dir)
#
#  #
#  # DO WORK ON DATA
#  #
#
#  print('%d data files containing %d records was loaded ' % (num_files, num_records))
#
#if __name__ == "__main__":
#	main()
