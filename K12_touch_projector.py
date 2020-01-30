#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import sys
import cv2
import numpy as np
from phone_operator import PhoneOperator
from const import const
from tp_utils import TPUtils


def main():
    global CAMERA_DEBUG_ENABLE
    if len(sys.argv) < 2:
        CAMERA_DEBUG_ENABLE = False
    elif len(sys.argv) == 2 and sys.argv[1] == '-d':
        CAMERA_DEBUG_ENABLE = True
    tputils = TPUtils()
    co_list = tputils.str_list_to_int(tputils.read_csv_data('co.conf'))
    global MAIN_CAMERA
    global TOP_CAMERA
    global TOUCH_THRESHOLD_LINE
    MAIN_CAMERA = co_list[6][0]
    TOP_CAMERA = co_list[6][1]
    TOUCH_THRESHOLD_LINE = co_list[4][1]
    # Set the capture order of the camera
    cap_i = [TOP_CAMERA, MAIN_CAMERA]
    camera_capture = []
    width = []
    height = []
    camera_count = len(cap_i)
    global phone_enable
    phone_enable = False
    is_touched = False
    last_touch = False
    need_touch_up = False
    is_landscape = False
    last_landscape = False
    # m_center_X = 0
    # m_center_Y = 0
    touch_down_time = time.time()
    route_in_camera = []
    route_in_phone = []
    p_opr = PhoneOperator(const.DEVICE_ID)
    switch = '0:La 1:Po'  # 0:Landscape 1:Portrait
    for i in range(0, camera_count):
        camera_capture.append(cv2.VideoCapture(int(cap_i[i])))
        # if i == MAIN_CAMERA & CAMERA_DEBUG_ENABLE:
        #     camera_capture[i].set(cv2.CAP_PROP_FRAME_WIDTH, po.PHONE_HEIGHT * po.RESOLUTION_ADAPT)
        #     camera_capture[i].set(cv2.CAP_PROP_FRAME_HEIGHT, po.PHONE_WIDTH * po.RESOLUTION_ADAPT)
        width.append(int(camera_capture[i].get(cv2.CAP_PROP_FRAME_WIDTH)))
        height.append(int(camera_capture[i].get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print('height -- ' + str(i) + ' --: ' + str(height))
        print('width  -- ' + str(i) + ' --: ' + str(width))
        if CAMERA_DEBUG_ENABLE:
            cv2.namedWindow('capture' + str(i), cv2.WINDOW_NORMAL)
            # Create sliders to control HSV thresholds
            # cv2.createTrackbar('H_low' + str(i), 'capture' + str(i), 0, 180, nothing)
            # cv2.createTrackbar('H_high' + str(i), 'capture' + str(i), 0, 18, nothing)
            # cv2.createTrackbar('S_low' + str(i), 'capture' + str(i), 170, 255, nothing)
            # cv2.createTrackbar('S_high' + str(i), 'capture' + str(i), 0, 255, nothing)
            # cv2.createTrackbar('V_low' + str(i), 'capture' + str(i), 205, 255, nothing)
            # cv2.createTrackbar('V_high' + str(i), 'capture' + str(i), 0, 255, nothing)
        if i == MAIN_CAMERA & CAMERA_DEBUG_ENABLE:
            # Create switch for Landscape/Portrait functionality, currently auto detect the screen orientation
            cv2.createTrackbar(switch, 'capture' + str(i), 0, 2, nothing)
        if not p_opr.is_phone_connected():
            phone_enable = False
        else:
            phone_enable = True
            is_landscape = p_opr.check_orientation(last_landscape)
            last_landscape = is_landscape

    index = 0
    n = 3  # take the average of 3 brightness Value
    m = 4 + 4
    t = [[0] * n] * m  # Fill an 8 by 3 array with all 0
    last_fake_landscape = False
    while True:
        for i in range(0, camera_count):
            starttime = time.time()
            _, capture_frame = camera_capture[int(cap_i[i])].read()

            hand_mask = bgr_2_hsv(capture_frame, i)
            if i == TOP_CAMERA & CAMERA_DEBUG_ENABLE:
                draw_top_camera_touch_threshold(capture_frame, i)
            if i == MAIN_CAMERA:
                fake_landscape = auto_get_landscape_by_hsv(capture_frame, i, t)
                if CAMERA_DEBUG_ENABLE:
                    check_camera_conners(capture_frame, i, p_opr)
                    cv2.setTrackbarPos(switch, 'capture' + str(i), fake_landscape)
                if fake_landscape != last_fake_landscape:
                    is_landscape = p_opr.check_orientation(last_landscape)
                    last_landscape = is_landscape
                    last_fake_landscape = fake_landscape

            centers = get_centers(hand_mask)  # 取中心点

            if len(centers) == 0:
                # print('len(centers) == 0: i=' + str(i) + ' frm idx:' + str(index) + ' route_in_camera: ' + str(route_in_camera))
                if i == TOP_CAMERA:
                    if (time.time() - touch_down_time) > 0.45:
                        if is_touched:
                            need_touch_up = True
                            is_touched = False
                        if CAMERA_DEBUG_ENABLE:
                            route_in_camera.clear()
                elif i == MAIN_CAMERA:
                    if need_touch_up:
                        touch_up(p_opr, route_in_camera, route_in_phone, is_landscape)
                        need_touch_up = False
                    if len(route_in_camera) > 0:
                        draw_trajectory(capture_frame, route_in_camera)
                        pass

            else:  # Capture the feature point
                count_centers = len(centers)
                if i == TOP_CAMERA:
                    total_aux_X = 0
                    total_aux_Y = 0
                    max_aux_Y = 0
                    for center in centers:
                        cv2.circle(capture_frame, center, 3, (0, 255, 0), 2)
                        total_aux_X += center[0]
                        total_aux_Y += center[1]
                        if center[1] > max_aux_Y:
                            max_aux_Y = center[1]
                    m_center_X = int(total_aux_X / count_centers)
                    aux_Y = int(total_aux_Y / count_centers)
                    if max_aux_Y > TOUCH_THRESHOLD_LINE:
                        # time_log('frm idx:' + str(index) + ' center: ' + str(center) + ' count_centers: ' + str(count_centers))
                        is_touched = True
                    elif max_aux_Y < TOUCH_THRESHOLD_LINE-10:
                        is_touched = False
                    # if aux_Y > 115:
                    # print('i=' + str(i) + ' frm idx:' + str(index) + ' m_center_X: ' + str(m_center_X) + ' aux_Y: ' + str(aux_Y) + ' is_touched: ' + str(is_touched))
                elif i == MAIN_CAMERA:
                    total_center_X = 0
                    total_center_Y = 0
                    for center in centers:
                        cv2.circle(capture_frame, center, 3, (0, 255, 0), 2)
                        total_center_X += center[0]
                        total_center_Y += center[1]
                    m_center_X = int(total_center_X / count_centers)
                    m_center_Y = int(total_center_Y / count_centers)
                    # print('capture=' + str(i) + ' frm idx:' + str(index) + ' m_center_X: ' + str(m_center_X) + ' m_center_Y: ' + str(m_center_Y) + ' count_centers: ' + str(count_centers) + ' centers: ' + str(centers))

                    if is_touched:
                        if CAMERA_DEBUG_ENABLE:
                            route_in_camera.append((m_center_X, m_center_Y))
                            draw_trajectory(capture_frame, route_in_camera)
                        if phone_enable:
                            if (not is_landscape and m_center_X > p_opr.PHONE_LEFT_TOP[0] and m_center_X <
                                p_opr.PHONE_RIGHT_BOTTOM[0] and m_center_Y > p_opr.PHONE_LEFT_TOP[1] and m_center_Y <
                                p_opr.PHONE_RIGHT_BOTTOM[1]) \
                                    or (is_landscape and m_center_X > p_opr.PHONE_LANDSCAPE_LEFT_TOP[0] and m_center_X <
                                        p_opr.PHONE_LANDSCAPE_RIGHT_BOTTOM[0] and m_center_Y >
                                        p_opr.PHONE_LANDSCAPE_LEFT_TOP[1] and m_center_Y <
                                        p_opr.PHONE_LANDSCAPE_RIGHT_BOTTOM[1]):
                                route_in_phone.append((m_center_X, m_center_Y))
                                if not last_touch:
                                    last_touch = touch_down(p_opr, (m_center_X, m_center_Y), touch_down_time, is_landscape)
                                else:
                                    last_touch = touch_move(p_opr, (m_center_X, m_center_Y), is_landscape)
                            # time_log(' i: ' + str(i) + ' is_touched: ' + str(is_touched) + ' last_touch: ' + str(last_touch) + ' is_landscape: ' + str(is_landscape))
                    elif last_touch:  # is_touched = False
                        last_touch = touch_up(p_opr, route_in_camera, route_in_phone, is_landscape)

            if CAMERA_DEBUG_ENABLE:
                cv2.imshow('capture' + str(i), capture_frame)
            index += 1

        if CAMERA_DEBUG_ENABLE:
            key = cv2.waitKey(10)
            if int(key) == 113:  # key q
                break
            elif int(key) == 112:  # key p
                cmd = 'adb shell input keyevent 26'  # KEY_POWER
                tputils.adb_os_system(cmd)
    for k in range(0, camera_count):
        camera_capture[int(cap_i[k])].release()
    cv2.destroyAllWindows()
    pass


def auto_get_landscape_by_hsv(capture_frame, i, t):
    orientation = False
    if i == MAIN_CAMERA:
        starttime = time.time()
        l_t_v_mean = int((t[0][0] + t[0][1] + t[0][2]) / 3)
        r_t_v_mean = int((t[1][0] + t[1][1] + t[1][2]) / 3)
        l_b_v_mean = int((t[2][0] + t[2][1] + t[2][2]) / 3)
        r_b_v_mean = int((t[3][0] + t[3][1] + t[3][2]) / 3)
        o_l_t_h, o_l_t_s, o_l_t_v = item_to_hsv(capture_frame, (18, 36))
        left_top_h, left_top_s, left_top_v = item_to_hsv(capture_frame, (18, 76))
        o_r_t_h, o_r_t_s, o_r_t_v = item_to_hsv(capture_frame, (620, 46))
        right_top_h, right_top_s, right_top_v = item_to_hsv(capture_frame, (620, 86))
        o_l_b_h, o_l_b_s, o_l_b_v = item_to_hsv(capture_frame, (18, 426))
        left_bottom_h, left_bottom_s, left_bottom_v = item_to_hsv(capture_frame, (18, 386))
        o_r_b_h, o_r_b_s, o_r_b_v = item_to_hsv(capture_frame, (620, 426))
        right_bottom_h, right_bottom_s, right_bottom_v = item_to_hsv(capture_frame, (620, 386))
        count = 0
        value_threshold = 40
        if abs(l_t_v_mean - o_l_t_v) > value_threshold:
            count += 1
        if abs(r_t_v_mean - o_r_t_v) > value_threshold:
            count += 1
        if abs(l_b_v_mean - o_l_b_v) > value_threshold:
            count += 1
        if abs(r_b_v_mean - o_r_b_v) > value_threshold:
            count += 1
        if count > 2:
            orientation = True
        else:
            orientation = False
        for i in range(0, 4):
            t[i][0] = t[i][1]
            t[i][1] = t[i][2]
        t[0][2] = left_top_v
        t[1][2] = right_top_v
        t[2][2] = left_bottom_v
        t[3][2] = right_bottom_v
        # print('fake_orientation:', orientation, 'o_l_t_v:', int(o_l_t_v), 'o_r_t_v:', int(o_r_t_v), 'o_l_b_v:', int(o_l_b_v), 'o_r_b_v:', int(o_r_b_v))
        # print('fake_orientation:', orientation, 'l_t_v_mean:', int(l_t_v_mean), 'r_t_v_mean:', int(r_t_v_mean), 'l_b_v_mean:', int(l_b_v_mean), 'r_b_v_mean:', int(r_b_v_mean))
        # print('auto_get_landscape_by_saturation state:', landscape, ' takes: ', (time.time() - starttime))
    return orientation


def check_camera_conners(capture_frame, i, po):
    if i == MAIN_CAMERA:
        # Show corner locations in portrait
        cv2.line(capture_frame, (po.PHONE_LEFT_TOP[0], po.PHONE_LEFT_TOP[1]),
                 (po.PHONE_LEFT_TOP[0] + 10, po.PHONE_LEFT_TOP[1]), (0, 255, 0), 2)
        cv2.line(capture_frame, (po.PHONE_LEFT_TOP[0], po.PHONE_LEFT_TOP[1]),
                 (po.PHONE_LEFT_TOP[0], po.PHONE_LEFT_TOP[1] + 10), (0, 255, 0), 2)
        cv2.line(capture_frame, (po.PHONE_RIGHT_BOTTOM[0], po.PHONE_RIGHT_BOTTOM[1]),
                 (po.PHONE_RIGHT_BOTTOM[0] - 10, po.PHONE_RIGHT_BOTTOM[1]), (0, 255, 0), 2)
        cv2.line(capture_frame, (po.PHONE_RIGHT_BOTTOM[0], po.PHONE_RIGHT_BOTTOM[1]),
                 (po.PHONE_RIGHT_BOTTOM[0], po.PHONE_RIGHT_BOTTOM[1] - 10), (0, 255, 0), 2)
        # Show corner locations in landscape
        cv2.line(capture_frame, (po.PHONE_LANDSCAPE_LEFT_TOP[0], po.PHONE_LANDSCAPE_LEFT_TOP[1]),
                 (po.PHONE_LANDSCAPE_LEFT_TOP[0] + 10, po.PHONE_LANDSCAPE_LEFT_TOP[1]), (0, 255, 0), 2)
        cv2.line(capture_frame, (po.PHONE_LANDSCAPE_LEFT_TOP[0], po.PHONE_LANDSCAPE_LEFT_TOP[1]),
                 (po.PHONE_LANDSCAPE_LEFT_TOP[0], po.PHONE_LANDSCAPE_LEFT_TOP[1] + 10), (0, 255, 0), 2)
        cv2.line(capture_frame, (po.PHONE_LANDSCAPE_RIGHT_BOTTOM[0], po.PHONE_LANDSCAPE_RIGHT_BOTTOM[1]),
                 (po.PHONE_LANDSCAPE_RIGHT_BOTTOM[0] - 10, po.PHONE_LANDSCAPE_RIGHT_BOTTOM[1]), (0, 255, 0), 2)
        cv2.line(capture_frame, (po.PHONE_LANDSCAPE_RIGHT_BOTTOM[0], po.PHONE_LANDSCAPE_RIGHT_BOTTOM[1]),
                 (po.PHONE_LANDSCAPE_RIGHT_BOTTOM[0], po.PHONE_LANDSCAPE_RIGHT_BOTTOM[1] - 10), (0, 255, 0), 2)


def draw_top_camera_touch_threshold(capture_frame, i):
    cv2.line(capture_frame, (0, TOUCH_THRESHOLD_LINE), (640, TOUCH_THRESHOLD_LINE), (0, 255, 0), 2)


def item_to_hsv(capture_frame, item_point):
    blue = capture_frame.item(item_point[1], item_point[0], 0)
    green = capture_frame.item(item_point[1], item_point[0], 1)
    red = capture_frame.item(item_point[1], item_point[0], 2)
    hue, saturation, value = rgb2hsv(red, green, blue)
    cv2.circle(capture_frame, (item_point[0], item_point[1]), 2, (0, 255, 0), 0)
    return hue, saturation, value


def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    m = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        if g >= b:
            h = ((g-b)/m)*60
        else:
            h = ((g-b)/m)*60 + 360
    elif mx == g:
        h = ((b-r)/m)*60 + 120
    elif mx == b:
        h = ((r-g)/m)*60 + 240
    if mx == 0:
        s = 0
    else:
        s = m/mx
    v = mx
    H = h / 2
    S = s * 255.0
    V = v * 255.0
    return H, S, V


def bgr_2_hsv(img, i):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # H_low_v_R = cv2.getTrackbarPos('H_low' + str(i), 'capture' + str(i))
    # H_high_v_R = cv2.getTrackbarPos('H_high' + str(i), 'capture' + str(i))
    # S_high_v = cv2.getTrackbarPos('S_high' + str(i), 'capture' + str(i))
    # V_high_v = cv2.getTrackbarPos('V_high' + str(i), 'capture' + str(i))
    # S_low_v = cv2.getTrackbarPos('S_low' + str(i), 'capture' + str(i))
    # V_low_v = cv2.getTrackbarPos('V_low' + str(i), 'capture' + str(i))
    # For red light
    H_low_v_R = 0
    H_high_v_R = 12
    # For blue light
    # H_low_v_B = 96
    # H_high_v_B = 108
    if i == TOP_CAMERA:
        S_low_v = 100
        V_low_v = 210
    elif i == MAIN_CAMERA:
        S_low_v = 187
        V_low_v = 207

    S_high_v = 255
    V_high_v = 255
    lower_skin_R = np.array([H_low_v_R, S_low_v, V_low_v])
    upper_skin_R = np.array([H_high_v_R, S_high_v, V_high_v])
    # mask_R -> 1 filter red channel
    mask_R = cv2.inRange(hsv, lower_skin_R, upper_skin_R)
    # mask_B -> 1 filter blue channel
    # lower_skin_B = np.array([H_low_v_B, S_low_v, V_low_v])
    # upper_skin_B = np.array([H_high_v_B, S_high_v, V_high_v])
    # mask_B = cv2.inRange(hsv, lower_skin_B, upper_skin_B)
    mask = mask_R \
           # | mask_B
    return mask


def get_centers(img):
    kernel = np.ones((5, 5), np.uint8)
    # closed = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    _, contours, h = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    vaild_centers = []
    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)  # Take the width and height coordinate outside the contour
        # print(' x: ' + str(x) + ' y: ' + str(y) + ' w: ' + str(w) + ' h: ' + str(h))
        vaild_centers.append((int(x+w/2), int(y+h/2)))
    return vaild_centers



def touch_down(po, center, touch_down_time, orientation):
    if phone_enable:
        x, y = po.cvt_to_phone(center, orientation)
        po.phone_touch_down(x, y)
        touch_down_time = time.time()
    return True


def touch_move(po, center, orientation):
    if phone_enable:
        x, y = po.cvt_to_phone(center, orientation)
        po.phone_touch_move(x, y)
    return True


def touch_up(po, route, p_route, orientation):
    if phone_enable and len(p_route) > 0:
        x, y = po.cvt_to_phone(p_route[-1], orientation)
        po.phone_touch_up(x, y)
    route.clear()
    p_route.clear()
    return False


def draw_trajectory(image_np, route):
    # print('route: ' + str(route))
    if len(route) > 1:
        for i in range(1, len(route)):
          cv2.line(image_np, route[i-1], route[i], (0, 255, 255), 2)
    pass


def time_log(log_str):
    print(str(time.ctime()) + " : " + log_str + ' t_ms: ' + str(time.time()))
    pass


def nothing(x):
    pass


if __name__ == '__main__':
    main()
