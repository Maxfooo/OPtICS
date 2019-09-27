import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

from .constants import *

#
# Set the dtype for bools in lrads
# NOTE: Bools have been set to uint8 and int32 at 
# different times
# 
bool_dtype = np.uint8

#
# Data types common to all tasks
#
fw_timers_dtype = np.dtype([
  ('control',     np.uint32),
  ('tick_10ns',   np.uint32),
  ('tick_1us',    np.uint32),
  ('tick_1ms',    np.uint32),
  ])

fw_regs_dtype = np.dtype([
  ('control',     np.uint32),
  ('test',        np.uint32),
  ('fw_rate',     np.uint32),
  ('fw_version',  np.uint32),
  ('status',      np.uint32),
  ('miss_count',  np.uint32),
  ('timers',      fw_timers_dtype),
  ])

task_stats_dtype = np.dtype([
  ('start',       np.uint32),
  ('stop',        np.uint32),
  ('delay',       np.uint32),
  ])

#
# Thermal and current control dtypes
#

tc_log_dtype = np.dtype([
  ('enabled',       bool_dtype),
  ('stuck_sensor',  bool_dtype),
  ('setpoint',      np.float32),
  ('feedback',      np.float32),
  ('correction',    np.float32),
  ])

cc_log_dtype = np.dtype([
  ('enabled',       bool_dtype),
  ('setpoint',      np.float32),
  ('feedback',      np.float32),
  ('correction',    np.float32),
  ])

#
# Master laser control dtypes
#

well_stats_dtype = np.dtype([
  ('scan_dir',        np.int32),
  ('wells_valid',     bool_dtype),
  ('wells_midpoint',  np.float32),
  ('wells_spacing',   np.float32),
  ('bow',             np.float32, NUM_WELLS),
  ('cow',             np.float32, NUM_WELLS),
  ('wow',             np.float32, NUM_WELLS),
  ])

mode_hop_stats_dtype = np.dtype([
  ('mode_hop',        bool_dtype),
  ('position',        np.float32),
  ])

ml_cmd_dtype = np.dtype([
  ('over_fsm',        bool_dtype),
  ('characterize',    bool_dtype),
  ('temp',            np.float32),
  ('current',         np.float32),
  ('amplitude',       np.float32),
  ('offset',          np.float32),
  ('phase',           np.float32),
  ])

ENV_ARR_SIZE  = 50
ml_status_dtype = np.dtype([
  ('state',             np.int32),
  ('wells_valid',       bool_dtype),
  ('wells_midpoint',    np.float32),
  ('well_center_sp',    np.float32),
  ('well_center_corr',  np.float32),
  ('temp_stable',       bool_dtype),
  ('temp_sp',           np.float32),
  ('temp',              np.float32),
  ('temp_std_dev',      np.float32),
  ('pressure',          np.float32),
  ('current',           np.float32),
  ('amplitude',         np.float32),
  ('offset',            np.float32),
  ('phase',             np.float32),
  ('up_scan_stable',    np.uint8),
  ('down_scan_stable',  np.uint8),
  ('op_env',            np.uint8, ENV_ARR_SIZE * ENV_ARR_SIZE),
  ])

hys_control_dtype = np.dtype([
  ('state',           np.int32),
  ('val',             np.float32),
  ('lock_pt',         np.float32),
  ('output',          np.float32),
  ('direction',       np.float32),
  ('faulted',         bool_dtype),
  ('enabled',         bool_dtype),
  ])

mlc_dtype = np.dtype([
  ('well_stats',        well_stats_dtype),
  ('mode_hop_stats',    mode_hop_stats_dtype),
  ('ml_cmd',            ml_cmd_dtype),
  ('ml_status',         ml_status_dtype),
  ('well_lock_status',  hys_control_dtype),
  ('mode_lock_status',  hys_control_dtype),
  ])

#
# Data processing / liblrads dtypes
#

wcs_dtype = np.dtype([
  ('center',              np.float32),
  ('width',               np.float32),
  ('shift',               np.float32),
  ('bottom',              np.float32),
  ('bottom_filtered',     np.float32),
  ('curvature',           np.float32),
  ('curvature_filtered',  np.float32),
  ('left_pt',             np.float32),
  ('right_pt',            np.float32),
  ('snr',                 np.float32),
  ])

measurements_dtype = np.dtype([
  ('LOS', np.float32, NUM_CHS),
  ('U',   np.float32),
  ('V',   np.float32),
  ('W',   np.float32),
  ('AOA', np.float32),
  ('AOS', np.float32),
  ('T',   np.float32),
  ('P',   np.float32),
  ])

#
# Main data types
#

io_dtype = np.dtype([
  ('fw_regs',             fw_regs_dtype),
  ('task_stats',          task_stats_dtype),
  ('scan_dir',            np.int32),
  ('cell_tips',           tc_log_dtype, NUM_CHS),
  ('cell_bodies',         tc_log_dtype, NUM_CHS),
  ('lasers_tc',           tc_log_dtype, NUM_LASERS),
  ('daylight_filters',    tc_log_dtype, NUM_DAYLIGHT_FILTERS),
  ('transceiver_heater',  tc_log_dtype),
  ('ref_tip',             tc_log_dtype),
  ('ref_body',            tc_log_dtype),
  ('lasers_cc',           cc_log_dtype, NUM_LASERS),
  ('mlc',                 mlc_dtype),
  ])

data_dtype = np.dtype([
  ('fw_regs',         fw_regs_dtype),
  ('scan_count',      np.uint32),
  ('scan_bin',        np.uint32),
  ('task_stats',      task_stats_dtype),
  ('ch1',             np.uint8, LEN_SCAN),
  ('ch2',             np.uint8, LEN_SCAN),
  ('ch3',             np.uint8, LEN_SCAN),
  ('ch4',             np.uint8, LEN_SCAN),
  ('bak1',            np.uint8, LEN_SCAN),
  ('bak2',            np.uint8, LEN_SCAN),
  ('bak3',            np.uint8, LEN_SCAN),
  ('bak4',            np.uint8, LEN_SCAN),
  ('master',          np.int16, LEN_SCAN),
  ('preamp',          np.int16, LEN_SCAN),
  ('master_power',    np.int16, LEN_SCAN),
  ('preamp_power',    np.int16, LEN_SCAN),
  ('ch1_filtered',    np.float32, LEN_SCAN),
  ('ch2_filtered',    np.float32, LEN_SCAN),
  ('ch3_filtered',    np.float32, LEN_SCAN),
  ('ch4_filtered',    np.float32, LEN_SCAN),
  ('master_filtered', np.float32, LEN_SCAN),
  ('preamp_filtered', np.float32, LEN_SCAN),
  ('backgrounds',     np.float32, NUM_CHS),
  ('scan_dir',        np.int32),
  ('wcs_ref',         wcs_dtype, NUM_WELLS),
  ('wcs_ch1',         wcs_dtype, NUM_WELLS),
  ('wcs_ch2',         wcs_dtype, NUM_WELLS),
  ('wcs_ch3',         wcs_dtype, NUM_WELLS),
  ('wcs_ch4',         wcs_dtype, NUM_WELLS),
  ('measurements',    measurements_dtype),
  ])


LEN_TS_STR = 128 # bytes
logger_dtype = np.dtype([
  ('fw_regs',     fw_regs_dtype),
  ('task_stats',  task_stats_dtype),
  ('scan_dir',    np.int32),
  ('ts_hours',    np.double),
  ('ts_seconds',  np.double),
  ('ts_str',      np.uint8, LEN_TS_STR),
  ])

#
# The final/full data
#
lrads_dtype = np.dtype([
  ('io',    io_dtype),
  ('data',  data_dtype),
  ('log',   logger_dtype),
  ])


#
# Helper routine to show dtype sizes
#
def _print_dtype_size(dt_name, dt):
  print('%20s: %d' % (dt_name.strip('_dtype'), dt.itemsize))

#
# Print all dtype sizes for visual inspection
#
def print_dtype_sizes():
  print('Generic')
  _print_dtype_size('fw_regs',               fw_regs_dtype)
  _print_dtype_size('fw_timers',             fw_timers_dtype)
  _print_dtype_size('task_stats',            task_stats_dtype)
  print('Thermal & Current Control')        
  _print_dtype_size('tc_log',                tc_log_dtype)
  _print_dtype_size('cc_log',                cc_log_dtype)
  print('Master Laser Control')
  _print_dtype_size('well_stats',            well_stats_dtype)
  _print_dtype_size('mode_hop_stats_dtype',  mode_hop_stats_dtype)
  _print_dtype_size('ml_cmd_dtype',          ml_cmd_dtype)
  _print_dtype_size('ml_status_dtype',       ml_status_dtype)
  _print_dtype_size('hys_control_dtype',     hys_control_dtype)
  _print_dtype_size('mlc_dtype',             mlc_dtype)
  print('Data Processing')
  _print_dtype_size('wcs',                   wcs_dtype)
  _print_dtype_size('measurements',          measurements_dtype)
  print('Tasks')
  _print_dtype_size('io',                    io_dtype)
  _print_dtype_size('data',                  data_dtype)
  _print_dtype_size('logger',                logger_dtype)
  print('LRADS')
  _print_dtype_size('lrads',                 lrads_dtype)


