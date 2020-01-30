#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import os
from const import const


class TPUtils:

    def __init__(self):
        pass

    def read_csv_data(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                output_list = list(reader)
        else:
            output_list = [[224, 42], [416, 427], [1, 62], [639, 405], [0, 120], [1080, 1920], [1, 0]]
            self.write_csv_data(file_name, output_list)
        return output_list

    def write_csv_data(self, output_file, datas):
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            for data in datas:
                writer.writerow(data)

    def str_list_to_int(self, lists):
        co_list = []
        for str_row in lists:
            t_list = []
            for col in str_row:
                t_list.append(int(col))
            co_list.append(list.copy(t_list))  # deep copy
            t_list.clear()
        return co_list

    def adb_os_system(self, cmd_str):
        if not const.DEVICE_ID == '':
            cmd_str = 'adb -s ' + const.DEVICE_ID + cmd_str.split('adb')[1]
        os.system(cmd_str)

    def adb_os_popen(self, cmd_str):
        if not const.DEVICE_ID == '':
            cmd_str = 'adb -s ' + const.DEVICE_ID + cmd_str.split('adb')[1]
        output = os.popen(cmd_str)
        return output

    def error_log(log_str, function_name):
        # USE sys._getframe().f_code.co_name TO get the error function name
        print('===  E R R O R  ===\n')
        print('ERROR_LOG:', log_str)
        print('Please check the function[ ' + function_name + ' ]\n')
        pass
