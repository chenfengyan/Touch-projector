#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import time
from tp_utils import TPUtils
from const import const


class PhoneOperator:
    phone_type = ''
    RESOLUTION_ADAPT = 1
    DEVICE_ID = ''
    LAST_DOWN_TIME = 0
    output = 0

    def __init__(self, device_id):
        self.DEVICE_ID = device_id
        if self.DEVICE_ID == const.MY_DEVICE_ID_1:
            self.phone_type = 'phone_location_in_capture'


        self.tp_utils = TPUtils()
        self.update_operate_coordinates()
        if self.is_phone_connected():
            self.PHONE_WIDTH, self.PHONE_HEIGHT = self.get_width_height()
        self.events = self.tp_utils.read_csv_data('phone_events.conf')
        self.phone_touch_down_commands = self.events[2][1].split('\\n')
        self.phone_touch_move_commands = self.events[3][1].split('\\n')
        self.phone_touch_up_commands = self.events[4][1].split('\\n')
        self.phone_click_commands = self.events[5][1].split('\\n')
        pass

    def phone_touch_down(self, point_X, point_Y):
        with open('tmp_cmds', 'w', encoding='utf-8') as f:
            for command in self.phone_touch_down_commands:
                f.write(command.replace('START_X', str(point_X)).replace('START_Y', str(point_Y))+'\n')
        cmd = 'adb shell < tmp_cmds'
        self.tp_utils.adb_os_system(cmd)
        time_log('phone_touch_DOWN : (' + str(int(point_X)) + ', ' + str(int(point_Y)) + ')')
        self.LAST_DOWN_TIME = time.time()
        pass

    def phone_touch_move(self, point_X, point_Y):
        with open('tmp_cmds', 'w', encoding='utf-8') as f:
            for command in self.phone_touch_move_commands:
                f.write(command.replace('POINT_X', str(point_X)).replace('POINT_Y', str(point_Y))+'\n')
        cmd = 'adb shell < tmp_cmds'
        self.tp_utils.adb_os_system(cmd)
        time_log('phone_touch_MOVE : (' + str(int(point_X)) + ', ' + str(int(point_Y)) + ')')
        pass

    def phone_touch_up(self, point_X, point_Y):
        with open('tmp_cmds', 'w', encoding='utf-8') as f:
            for command in self.phone_touch_up_commands:
                f.write(command.replace('END_X', str(point_X)).replace('END_Y', str(point_Y))+'\n')
        cmd = 'adb shell < tmp_cmds'
        self.tp_utils.adb_os_system(cmd)
        time_log('phone_touch_UP   : (' + str(int(point_X)) + ', ' + str(int(point_Y)) + ') TAKES:' + ('%.2f' % (time.time() - self.LAST_DOWN_TIME)) + 'S')
        pass

    def phone_click(self, point_X, point_Y):
        with open('tmp_cmds', 'w', encoding='utf-8') as f:
            for command in self.phone_click_commands:
                f.write(command.replace('POINT_X', str(point_X)).replace('POINT_Y', str(point_Y))+'\n')
        cmd = 'adb shell < tmp_cmds'
        self.tp_utils.adb_os_system(cmd)
        time_log('phone_CLICK   : (' + str(int(point_X)) + ', ' + str(int(point_Y)) + ')')
        pass

    def cvt_to_phone(self, point, is_landscape):
        if not is_landscape:
            point_X = int((point[0] - self.PHONE_LEFT_TOP[0]) * self.PHONE_WIDTH * self.RESOLUTION_ADAPT / (self.PHONE_RIGHT_BOTTOM[0] - self.PHONE_LEFT_TOP[0]))
            point_Y = int((point[1] - self.PHONE_LEFT_TOP[1]) * self.PHONE_HEIGHT * self.RESOLUTION_ADAPT / (self.PHONE_RIGHT_BOTTOM[1] - self.PHONE_LEFT_TOP[1]))
        elif is_landscape:
            point_X = (self.PHONE_LANDSCAPE_RIGHT_BOTTOM[1] - point[1]) * self.PHONE_WIDTH * self.RESOLUTION_ADAPT / (
                        self.PHONE_LANDSCAPE_RIGHT_BOTTOM[1] - self.PHONE_LANDSCAPE_LEFT_TOP[1])
            point_Y = (point[0] - self.PHONE_LANDSCAPE_LEFT_TOP[0]) * self.PHONE_HEIGHT * self.RESOLUTION_ADAPT / (
                        self.PHONE_LANDSCAPE_RIGHT_BOTTOM[0] - self.PHONE_LANDSCAPE_LEFT_TOP[0])-(point[0] - 320)*0.1
        return point_X, point_Y

    def get_width_height(self):
        cmd = 'adb shell wm size'
        output = self.tp_utils.adb_os_popen(cmd)
        w_and_h = output.readline().split('size:')[1].strip()
        output.close()
        width = int(w_and_h.split('x')[0])
        height = int(w_and_h.split('x')[1])
        return width, height

    def update_operate_coordinates(self):
        co_list = self.tp_utils.str_list_to_int(self.tp_utils.read_csv_data('co.conf'))
        self.PHONE_LEFT_TOP = co_list[0]
        self.PHONE_RIGHT_BOTTOM = co_list[1]
        self.PHONE_LANDSCAPE_LEFT_TOP = co_list[2]
        self.PHONE_LANDSCAPE_RIGHT_BOTTOM = co_list[3]

    def check_orientation(self, last_orientation):
        starttime = time.time()
        current_orientation = False
        cmd = 'adb shell dumpsys window|findstr /i "mCurrentAppOrientation="'
        output = self.tp_utils.adb_os_popen(cmd)
        read_output = output.read()
        output.close()
        result = read_output.split('=')[1].strip()  # first letter after " = "
        if result == '0':
            current_orientation = True  # landscape True
        elif result == '1':
            current_orientation = False  # portrait False
        elif result == '5':
            current_orientation = False  # portrait False
        elif result == '-1':
            current_orientation = False  # portrait False
        else:
            self.tp_utils.error_log('did not get orientation result. output.read: ' + read_output, sys._getframe().f_code.co_name)
        if last_orientation != current_orientation:
            print('check_orientation :', 'Landscape' if current_orientation else 'Portrait', 'result:', result, 'takes:',
                  (time.time() - starttime))
        return current_orientation

    def is_phone_connected(self):
        cmd = 'adb devices'
        output = os.popen(cmd)
        if output.readlines()[1] == '\n':
            phone_connected = False
        else:
            phone_connected = True
        output.close()
        return phone_connected


def time_log(log_str):
    print(str(time.ctime()) + ' : ' + log_str + ' t_ms: ' + str(time.time()))
    pass
