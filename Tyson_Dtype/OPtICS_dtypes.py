import numpy as np

GPS_LENGTH = 0x0100

WellCharacteristics_dtype = np.dtype([
  ('center', np.float32),
  ('width', np.float32),
  ('shift', np.float32),
  ('bottom', np.float32),
  ('bottom_filtered', np.float32),
  ('curvature', np.float32),
  ('curvature_filtered', np.float32),
  ('left_pt', np.float32),
  ('right_pt', np.float32),
  ('snr', np.float32),
])

Measurements_dtype = np.dtype([
  ('LOS', np.float32, 4),
  ('U', np.float32),
  ('V', np.float32),
  ('W', np.float32),
  ('AOA', np.float32),
  ('AOS', np.float32),
  ('T', np.float32),
  ('P', np.float32),
])

LibLRADSOutputs_dtype = np.dtype([
  ('wcs_ref', WellCharacteristics_dtype),
  ('wcs_ch1', WellCharacteristics_dtype),
  ('wcs_ch2', WellCharacteristics_dtype),
  ('wcs_ch3', WellCharacteristics_dtype),
  ('wcs_ch4', WellCharacteristics_dtype),
  ('measurements', Measurements_dtype),
])

RawWellScans_dtype = np.dtype([
  ('ch1_signal', np.uint8, 1000),
  ('ch2_signal', np.uint8, 1000),
  ('ch3_signal', np.uint8, 1000),
  ('ch4_signal', np.uint8, 1000),
  ('ch1_background', np.uint8, 1000),
  ('ch2_background', np.uint8, 1000),
  ('ch3_background', np.uint8, 1000),
  ('ch4_background', np.uint8, 1000),
  ('master', np.int16, 1000),
  ('preamp', np.int16, 1000),
  ('master_power', np.int16, 1000),
  ('preamp_power', np.int16, 1000),
])

FilteredWellScans_dtype = np.dtype([
  ('ch1_filtered', np.float32, 1000),
  ('ch2_filtered', np.float32, 1000),
  ('ch3_filtered', np.float32, 1000),
  ('ch4_filtered', np.float32, 1000),
  ('master_filtered', np.float32, 1000),
  ('preamp_filtered', np.float32, 1000),
])

WellScans_dtype = np.dtype([
  ('raw_scans', RawWellScans_dtype),
  ('filtered_scans', FilteredWellScans_dtype),
])

TestRegister_dtype = np.dtype([
  ('word', np.uint32),
])

ControlRegister_dtype = np.dtype([
  ('word', np.uint32),
])

FirmwareVersion_dtype = np.dtype([
  ('minor', np.uint16),
  ('major', np.uint16),
])

FWTimers_dtype = np.dtype([
  ('control_reg', ControlRegister_dtype),
  ('tick_10ns', np.uint32),
  ('tick_1us', np.uint32),
  ('tick_1ms', np.uint32),
])

FirmwareRate_dtype = np.dtype([
  ('counts', np.uint32),
])

StatusRegister_dtype = np.dtype([
  ('word', np.uint32),
])

WellScanRegisters_dtype = np.dtype([
  ('ch1_signal', np.uint8, 0x2000),
  ('ch2_signal', np.uint8, 0x2000),
  ('ch3_signal', np.uint8, 0x2000),
  ('ch4_signal', np.uint8, 0x2000),
  ('ch1_background', np.uint8, 0x2000),
  ('ch2_background', np.uint8, 0x2000),
  ('ch3_background', np.uint8, 0x2000),
  ('ch4_background', np.uint8, 0x2000),
  ('ch1_filtered', np.uint8, 0x2000),
  ('ch2_filtered', np.uint8, 0x2000),
  ('ch3_filtered', np.uint8, 0x2000),
  ('ch4_filtered', np.uint8, 0x2000),
  ('master', np.uint8, 0x2000),
  ('preamp', np.uint8, 0x2000),
  ('master_power', np.uint8, 0x2000),
  ('preamp_power', np.uint8, 0x2000),
  ('master_filtered', np.uint8, 0x2000),
  ('master_power_filtered', np.uint8, 0x2000),
  ('preamp_filtered', np.uint8, 0x2000),
  ('preamp_power_filtered', np.uint8, 0x2000),
])

LoggerRegisters_dtype = np.dtype([
  ('control', ControlRegister_dtype),
  ('test', TestRegister_dtype),
  ('fw_rate', FirmwareRate_dtype),
  ('fw_version', FirmwareVersion_dtype),
  ('status', StatusRegister_dtype),
  ('miss_count', np.uint32),
  ('timers', FWTimers_dtype),
])

SimRef_dtype = np.dtype([
  ('power', np.int16),
  ('ref', np.int16),
])

SimCh_dtype = np.dtype([
  ('ch1', np.uint8),
  ('ch2', np.uint8),
  ('ch3', np.uint8),
  ('ch4', np.uint8),
])

SimDataRegisters_dtype = np.dtype([
  ('refs', SimRef_dtype),
  ('signals', SimCh_dtype),
  ('backgrounds', SimCh_dtype),
])

"""
LTCsManager_dtype = np.dtype([
  ('therm_0_ltcs', ),
  ('therm_1_ltcs', ),
  ('therm_2_ltcs', ),
  ('laser_ltcs', ),
])
"""

DataRegisters_dtype = np.dtype([
  ('control', ControlRegister_dtype),
  ('test', TestRegister_dtype),
  ('fw_rate', FirmwareRate_dtype),
  ('fw_version', FirmwareVersion_dtype),
  ('status', StatusRegister_dtype),
  ('miss_count', np.uint32),
  ('timers', FWTimers_dtype),
  ('scan_rate', np.uint32),
  ('piezo_rate', np.uint32),
  ('adc_rate', np.uint32),
  ('bin_rate', np.uint32),
  ('mod_time', np.uint32),
  ('scan_count', np.uint32),
  ('scan_bin', np.uint32),
  ('sys_prop_delay', np.uint32),
  ('master_laser_scan_amplitude', np.int16),
  ('blank_0', np.int16),
  ('master_laser_scan_offset', np.int16),
  ('blank_1', np.int16),
  ('master_laser_scan_phase', np.int16),
  ('blank_2', np.int16),
  ('fast_adcs', np.uint32, 8),
  ('pps_latch', np.uint32),
  ('timestamp_latch', np.uint32),
  ('preamp_dither_amplitude', np.int16),
  ('blank_3', np.int16),
  ('preamp_dither_offset', np.int16),
  ('blank_4', np.int16),
  ('preamp_dither_phase', np.int16),
  ('blank_5', np.int16),
  ('amp0_dither_amplitude', np.int16),
  ('blank_6', np.int16),
  ('amp0_dither_offset', np.int16),
  ('blank_7', np.int16),
  ('amp0_dither_phase', np.int16),
  ('blank_8', np.int16),
  ('amp1_dither_amplitude', np.int16),
  ('blank_9', np.int16),
  ('amp1_dither_offset', np.int16),
  ('blank_10', np.int16),
  ('amp1_dither_phase', np.int16),
  ('blank_11', np.int16),
  ('ch1_background_up', np.uint32),
  ('ch1_background_down', np.uint32),
  ('ch2_background_up', np.uint32),
  ('ch2_background_down', np.uint32),
  ('ch3_background_up', np.uint32),
  ('ch3_background_down', np.uint32),
  ('ch4_background_up', np.uint32),
  ('ch4_background_down', np.uint32),
])

LTC_dtype = np.dtype([
])

LTC2983_Register_dtype = np.dtype([
  ('status', np.uint8),
  ('value', np.float32),
])

"""
DACsManager_dtype = np.dtype([
  ('therm_0_dacs', ),
  ('therm_1_dacs', ),
  ('therm_2_dacs', ),
  ('laser_dacs', ),
])
"""

Backgrounds_dtype = np.dtype([
  ('ch1', np.float32),
  ('ch2', np.float32),
  ('ch3', np.float32),
  ('ch4', np.float32),
])

"""
ADCsManager_dtype = np.dtype([
  ('laser_raw_adcs', ),
  ('laser_avg_adcs', ),
])
"""

FWTimersControlRegister_dtype = np.dtype([
  ('word', np.uint32),
])

LaserControl_dtype = np.dtype([
  ('dither_en', np.uint8),
  ('temperature', np.float32),
  ('amplitude', np.float32),
  ('offset', np.float32),
  ('phase', np.float32),
])

LaserControlSet_dtype = np.dtype([
  ('pre', LaserControl_dtype),
  ('amp0', LaserControl_dtype),
  ('amp1', LaserControl_dtype),
])

tc_log_t_dtype = np.dtype([
  ('enabled', np.uint8),
  ('stuckSensor', np.uint8),
  ('setpoint', np.float32),
  ('feedback', np.float32),
  ('correction', np.float32),
])

cc_log_t_dtype = np.dtype([
  ('enabled', np.uint8),
  ('setpoint', np.float32),
  ('feedback', np.float32),
  ('correction', np.float32),
])


CLITestData_dtype = np.dtype([
  ('a', np.int32),
  ('x', np.float32),
])

ThermalControlRegister_dtype = np.dtype([
  ('word', np.uint32),
])

IORegisters_dtype = np.dtype([
  ('control', ControlRegister_dtype),
  ('test', TestRegister_dtype),
  ('fw_rate', FirmwareRate_dtype),
  ('fw_version', FirmwareVersion_dtype),
  ('status', StatusRegister_dtype),
  ('miss_count', np.uint32),
  ('timers', FWTimers_dtype),
  ('therm_0_control', np.uint32),
  ('therm_0_dacs', np.int16, 16),
  ('therm_0_ltcs', np.uint32, 9),
  ('therm_1_control', np.uint32),
  ('therm_1_dacs', np.int16, 16),
  ('therm_1_ltcs', np.uint32, 9),
  ('therm_2_control', np.uint32),
  ('therm_2_dacs', np.int16, 16),
  ('therm_2_ltcs', np.uint32, 9),
  ('laser_control', np.uint32),
  ('laser_dacs', np.int16, 16),
  ('laser_ltcs', np.uint32, 9),
  ('laser_raw_adcs', np.int32, 8),
  ('laser_avg_adcs', np.int32, 8),
  ('ml_current_limit', np.uint32),
  ('preamp_current_limit', np.uint32),
  ('amp0_current_limit', np.uint32),
  ('amp1_current_limit', np.uint32),
  ('amplitude', np.int16),
  ('offset', np.int16),
  ('phase', np.int16),
])

UTC_dtype = np.dtype([
  ('year', np.uint32),
  ('month', np.uint32),
  ('day', np.uint32),
  ('hour', np.uint32),
  ('minute', np.uint32),
  ('second', np.float64),
  ('str', np.int8, 128),
])

ZDATime_dtype = np.dtype([
  ('h', np.uint32),
  ('m', np.uint32),
  ('s', np.uint32),
  ('ms', np.uint32),
])

ZDAFields_dtype = np.dtype([
  ('header', np.int8, 16),
  ('time', np.int8, 16),
  ('day', np.int8, 16),
  ('month', np.int8, 16),
  ('year', np.int8, 16),
  ('offset', np.int8, 16),
  ('CS', np.int8, 16),
])

ZDAData_dtype = np.dtype([
  ('sentence', np.int8, GPS_LENGTH),
  ('zda_ok', np.uint8),
  ('zdaFields', ZDAFields_dtype),
  ('zdaTime', ZDATime_dtype),
  ('year', np.uint32),
])

hys_control_log_dtype = np.dtype([
  ('state', np.int32),
  ('val', np.float32),
  ('lock_pt', np.float32),
  ('output', np.float32),
  ('direction', np.float32),
  ('faulted', np.uint8),
  ('enabled', np.uint8),
])

ml_cmd_t_dtype = np.dtype([
  ('ovr_fsm', np.uint8),
  ('temp', np.float32),
  ('current', np.float32),
  ('amplitude', np.float32),
  ('offset', np.float32),
  ('phase', np.float32),
])

ml_status_t_dtype = np.dtype([
  ('state', np.int32),
  ('wells_valid', np.uint8),
  ('wells_midpoint', np.float32),
  ('well_center_sp', np.float32),
  ('well_center_corr', np.float32),
  ('temp_stable', np.uint8),
  ('temp_sp', np.float32),
  ('temp', np.float32),
  ('temp_std_dev', np.float32),
  ('pressure', np.float32),
  ('current', np.float32),
  ('amplitude', np.float32),
  ('offset', np.float32),
  ('phase', np.float32),
  ('up_scan_stable', np.uint8),
  ('down_scan_stable', np.uint8),
])

well_stats_t_dtype = np.dtype([
  ('scan_dir', np.int32),
  ('wells_valid', np.uint8),
  ('wells_midpoint', np.float32),
  ('well_spacing', np.float32),
  ('bow', np.float32, 2),
  ('cow', np.float32, 2),
  ('wow', np.float32, 2),
])

mode_hop_stats_t_dtype = np.dtype([
  ('mode_hop', np.uint8),
  ('mh_pos', np.float32),
])

StableCond_dtype = np.dtype([
  ('started', np.uint8),
  ('start', np.int32),
  ('stop', np.int32),
  ('length', np.int32),
])

sockaddr_in_dtype = np.dtype([
])

SerialPacketData_dtype = np.dtype([
  ('packet_count', np.uint32),
  ('pass_count', np.uint32),
  ('fail_count', np.uint32),
])

VarTypes_dtype = np.dtype([
  ('v_int8_t', np.int8),
  ('v_int16_t', np.int16),
  ('v_int32_t', np.int32),
  ('v_int64_t', np.int64),
  ('v_uint8_t', np.uint8),
  ('v_uint16_t', np.uint16),
  ('v_uint32_t', np.uint32),
  ('v_uint64_t', np.uint64),
  ('v_char_t', np.int8),
  ('v_int_t', np.int32),
  ('v_long_t', np.int32),
  ('v_longlong_t', np.int64),
  ('v_float_t', np.float32),
  ('v_double_t', np.float64),
  ('v_uchar_t', np.uint8),
  ('v_uint_t', np.uint32),
  ('v_ulong_t', np.uint32),
  ('v_ulonglong_t', np.uint64),
  ('v_bool_t', np.uint8),
  ('v_string_t', np.int8),
])

HeaderMember_dtype = np.dtype([
  ('type', np.uint8),
  ('size', np.uint16),
  ('name', np.int8, 32),
])

PartitionMember_dtype = np.dtype([
  ('size', np.uint16),
  ('name', np.int8, 32),
])

timeval_dtype = np.dtype([
])

DateTime_dtype = np.dtype([
])

GUICmd_dtype = np.dtype([
  ('word', np.uint32),
])

amp_cmd_t_dtype = np.dtype([
  ('voltage', np.float32),
])

DataLoggedDataRaw_dtype = np.dtype([
  ('control', ControlRegister_dtype),
  ('test', TestRegister_dtype),
  ('fw_rate', FirmwareRate_dtype),
  ('fw_version', FirmwareVersion_dtype),
  ('status', StatusRegister_dtype),
  ('miss_count', np.uint32),
  ('timers', FWTimers_dtype),
  ('scan_count', np.uint32),
  ('scan_bin', np.uint32),
  ('start_time', np.uint32),
  ('stop_time', np.uint32),
  ('task_delay', np.uint32),
  ('raw_scans', RawWellScans_dtype),
  ('scan_dir', np.int32),
  ('wcs_ref', WellCharacteristics_dtype),
  ('wcs_1', WellCharacteristics_dtype),
  ('wcs_2', WellCharacteristics_dtype),
  ('wcs_3', WellCharacteristics_dtype),
  ('wcs_4', WellCharacteristics_dtype),
  ('measurements', Measurements_dtype),
])

GUIPkt_dtype = np.dtype([
])



FWState_dtype = np.dtype([
  ('control', ControlRegister_dtype),
  ('test', TestRegister_dtype),
  ('fw_rate', FirmwareRate_dtype),
  ('fw_version', FirmwareVersion_dtype),
  ('status', StatusRegister_dtype),
  ('miss_count', np.uint32),
  ('timers', FWTimers_dtype),
])

ClientStatus_dtype = np.dtype([
  ('word', np.int32),
])

ClientUDPData_dtype = np.dtype([
  ('utcTimeInSec', np.float64),
  ('measurements', Measurements_dtype),
  ('sig_strength', np.int32, 4),
  ('background', np.int32, 4),
  ('status', ClientStatus_dtype),
])

ClientLoggedData_dtype = np.dtype([
  ('raw_well_scans', RawWellScans_dtype),
  ('client_udp_data', ClientUDPData_dtype),
  ('timestampHour', np.float64),
  ('timestampStr', np.int8, 128),
])
MLControl_dtype = np.dtype([
  ('well_stats', well_stats_t_dtype),
  ('mode_hop_stats', mode_hop_stats_t_dtype),
  ('ml_cmd', ml_cmd_t_dtype),
  ('ml_status', ml_status_t_dtype),
  ('well_lock_status', hys_control_log_dtype),
  ('mode_lock_status', hys_control_log_dtype),
])

ioLoggedData_dtype = np.dtype([
  ('control', ControlRegister_dtype),
  ('test', TestRegister_dtype),
  ('fw_rate', FirmwareRate_dtype),
  ('fw_version', FirmwareVersion_dtype),
  ('status', StatusRegister_dtype),
  ('miss_count', np.uint32),
  ('timers', FWTimers_dtype),
  ('start_time', np.uint32),
  ('stop_time', np.uint32),
  ('task_delay', np.uint32),
  ('scan_dir', np.int32),
  ('cell_tip', tc_log_t_dtype),
  ('cell_body', tc_log_t_dtype),
  ('laser_temp', tc_log_t_dtype),
  ('day_filt', tc_log_t_dtype),
  ('xcvr', tc_log_t_dtype),
  ('ref_tip', tc_log_t_dtype),
  ('ref_body', tc_log_t_dtype),
  ('laser_current', cc_log_t_dtype),
  ('ml_control', MLControl_dtype),
])

DataLoggedData_dtype = np.dtype([
  ('control', ControlRegister_dtype),
  ('test', TestRegister_dtype),
  ('fw_rate', FirmwareRate_dtype),
  ('fw_version', FirmwareVersion_dtype),
  ('status', StatusRegister_dtype),
  ('miss_count', np.uint32),
  ('timers', FWTimers_dtype),
  ('scan_count', np.uint32),
  ('scan_bin', np.uint32),
  ('start_time', np.uint32),
  ('stop_time', np.uint32),
  ('task_delay', np.uint32),
  ('raw_scans', RawWellScans_dtype),
  ('filtered_scans', FilteredWellScans_dtype),
  ('backgrounds', Backgrounds_dtype),
  ('scan_dir', np.int32),
  ('wcs_ref', WellCharacteristics_dtype),
  ('wcs_1', WellCharacteristics_dtype),
  ('wcs_2', WellCharacteristics_dtype),
  ('wcs_3', WellCharacteristics_dtype),
  ('wcs_4', WellCharacteristics_dtype),
  ('measurements', Measurements_dtype),
])

LoggerLoggedData_dtype = np.dtype([
  ('control', ControlRegister_dtype),
  ('test', TestRegister_dtype),
  ('fw_rate', FirmwareRate_dtype),
  ('fw_version', FirmwareVersion_dtype),
  ('status', StatusRegister_dtype),
  ('miss_count', np.uint32),
  ('timers', FWTimers_dtype),
  ('start_time', np.uint32),
  ('stop_time', np.uint32),
  ('task_delay', np.uint32),
  ('scan_dir', np.int32),
  ('timestampHour', np.float64),
  ('timestampSeconds', np.float64),
])

DataOut_dtype = np.dtype([
  ('io_data', ioLoggedData_dtype),
  ('data_data', DataLoggedData_dtype),
  ('logger_data', LoggerLoggedData_dtype),
])

DataOutRaw_dtype = np.dtype([
  ('io_data', ioLoggedData_dtype),
  ('data_data', DataLoggedDataRaw_dtype),
  ('logger_data', LoggerLoggedData_dtype),
])

SharedDDR_dtype = np.dtype([
  ('data_out', DataOut_dtype),
  ('test_data', CLITestData_dtype),
  ('ml_control', MLControl_dtype),
  ('laser_control', LaserControlSet_dtype),
])