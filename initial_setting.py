#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
from phone_operator import PhoneOperator
from const import const
from tp_utils import TPUtils


class Ui_Touch_Projector_Setting(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)  # The constructor of the parent class

        self.timer_camera = QtCore.QTimer()  # Defines a timer to control the frame rate of a video display
        self.cap = cv2.VideoCapture()
        self.current_camera_number = 0
        self.p_opr = PhoneOperator(const.DEVICE_ID)
        self.tp_utils = TPUtils()
        self.co_list = self.tp_utils.str_list_to_int(self.tp_utils.read_csv_data('co.conf'))
        self.STEP = 2
        self.setupUi()  # Initializes the program interface
        print('co_list', self.co_list)

    '''Interface layout'''

    def setupUi(self):
        self.setObjectName("Touch_Projector_Setting")
        self.resize(800, 530)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 641, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.TopOptionsLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.TopOptionsLayout.setContentsMargins(10, 10, 10, 10)
        self.TopOptionsLayout.setObjectName("TopOptionsLayout")
        self.LandLeftTopPoint = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.LandLeftTopPoint.setObjectName("LandLeftTopPoint")
        self.TopOptionsLayout.addWidget(self.LandLeftTopPoint)
        self.PortLeftTopPoint = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.PortLeftTopPoint.setObjectName("PortLeftTopPoint")
        self.TopOptionsLayout.addWidget(self.PortLeftTopPoint)
        self.PortRightBottomPoint = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.PortRightBottomPoint.setObjectName("PortRightBottomPoint")
        self.TopOptionsLayout.addWidget(self.PortRightBottomPoint)
        self.LandRightBottomPoint = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.LandRightBottomPoint.setObjectName("LandRightBottomPoint")
        self.TopOptionsLayout.addWidget(self.LandRightBottomPoint)
        self.TouchDivider = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.TouchDivider.setObjectName("TouchDivider")
        self.TopOptionsLayout.addWidget(self.TouchDivider)
        self.ButtonFrame = QtWidgets.QFrame(self.centralwidget)
        self.ButtonFrame.setGeometry(QtCore.QRect(640, 0, 151, 521))
        self.ButtonFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ButtonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ButtonFrame.setObjectName("ButtonFrame")
        self.ButtonRight = QtWidgets.QPushButton(self.ButtonFrame)
        self.ButtonRight.setGeometry(QtCore.QRect(70, 60, 51, 31))
        self.ButtonRight.setObjectName("ButtonRight")
        self.ButtonDown = QtWidgets.QPushButton(self.ButtonFrame)
        self.ButtonDown.setGeometry(QtCore.QRect(40, 100, 51, 31))
        self.ButtonDown.setObjectName("ButtonDown")
        self.ButtonUp = QtWidgets.QPushButton(self.ButtonFrame)
        self.ButtonUp.setGeometry(QtCore.QRect(40, 20, 51, 31))
        self.ButtonUp.setObjectName("ButtonUp")
        self.ButtonLeft = QtWidgets.QPushButton(self.ButtonFrame)
        self.ButtonLeft.setGeometry(QtCore.QRect(10, 60, 51, 31))
        self.ButtonLeft.setObjectName("ButtonLeft")
        self.ButtonOpenCamera = QtWidgets.QPushButton(self.ButtonFrame)
        self.ButtonOpenCamera.setGeometry(QtCore.QRect(20, 200, 91, 31))
        self.ButtonOpenCamera.setObjectName("ButtonOpenCamera")
        self.ButtonSaveExit = QtWidgets.QPushButton(self.ButtonFrame)
        self.ButtonSaveExit.setGeometry(QtCore.QRect(20, 470, 91, 31))
        self.ButtonSaveExit.setObjectName("ButtonSaveExit")
        self.currCamNum = QtWidgets.QLabel(self.ButtonFrame)
        self.currCamNum.setGeometry(QtCore.QRect(10, 155, 91, 31))
        self.currCamNum.setObjectName("currCamNum")
        self.comboCurrCamNum = QtWidgets.QComboBox(self.ButtonFrame)
        self.comboCurrCamNum.setGeometry(QtCore.QRect(100, 160, 41, 22))
        self.comboCurrCamNum.setObjectName("comboCurrCamNum")
        self.comboCurrCamNum.addItem("")
        self.comboCurrCamNum.addItem("")
        self.ButtonRefreshResolution = QtWidgets.QPushButton(self.ButtonFrame)
        self.ButtonRefreshResolution.setGeometry(QtCore.QRect(20, 350, 111, 28))
        self.ButtonRefreshResolution.setObjectName("ButtonRefreshResolution")
        self.phonePixels = QtWidgets.QLabel(self.ButtonFrame)
        self.phonePixels.setGeometry(QtCore.QRect(20, 390, 121, 16))
        self.phonePixels.setObjectName("phonePixels")
        self.cameraLabel = QtWidgets.QLabel(self.ButtonFrame)
        self.cameraLabel.setGeometry(QtCore.QRect(10, 270, 131, 16))
        self.cameraLabel.setObjectName("cameraLabel")
        self.comboMainCamera = QtWidgets.QComboBox(self.ButtonFrame)
        self.comboMainCamera.setGeometry(QtCore.QRect(10, 300, 41, 22))
        self.comboMainCamera.setObjectName("comboMainCamera")
        self.comboMainCamera.addItem("")
        self.comboMainCamera.addItem("")
        self.comboMainCamera.addItem("")
        self.comboTopCamera = QtWidgets.QComboBox(self.ButtonFrame)
        self.comboTopCamera.setGeometry(QtCore.QRect(80, 300, 41, 22))
        self.comboTopCamera.setObjectName("comboTopCamera")
        self.comboTopCamera.addItem("")
        self.comboTopCamera.addItem("")
        self.comboTopCamera.addItem("")
        self.label_show_camera = QtWidgets.QLabel(self.centralwidget)
        self.label_show_camera.setGeometry(QtCore.QRect(0, 40, 641, 481))
        self.label_show_camera.setObjectName("label_show_camera")
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Touch_Projector_Setting", "触控投影设置"))
        self.LandLeftTopPoint.setText(_translate("Touch_Projector_Setting", "横屏左上角点"))
        self.PortLeftTopPoint.setText(_translate("Touch_Projector_Setting", "竖屏左上角点"))
        self.PortRightBottomPoint.setText(_translate("Touch_Projector_Setting", "竖屏右下角点"))
        self.LandRightBottomPoint.setText(_translate("Touch_Projector_Setting", "横屏右下角点"))
        self.TouchDivider.setText(_translate("Touch_Projector_Setting", "触控分隔线"))
        self.ButtonRight.setText(_translate("Touch_Projector_Setting", "右"))
        self.ButtonDown.setText(_translate("Touch_Projector_Setting", "下"))
        self.ButtonUp.setText(_translate("Touch_Projector_Setting", "上"))
        self.ButtonLeft.setText(_translate("Touch_Projector_Setting", "左"))
        self.ButtonOpenCamera.setText(_translate("Touch_Projector_Setting", "开启摄像头"))
        self.ButtonSaveExit.setText(_translate("Touch_Projector_Setting", "保存退出"))
        self.currCamNum.setText(_translate("Touch_Projector_Setting", "选择摄像头:"))
        self.comboCurrCamNum.setItemText(0, _translate("Touch_Projector_Setting", "0"))
        self.comboCurrCamNum.setItemText(1, _translate("Touch_Projector_Setting", "1"))
        self.ButtonRefreshResolution.setText(_translate("Touch_Projector_Setting", "刷新手机分辨率"))
        self.phonePixels.setText(_translate("Touch_Projector_Setting", "宽:1080 高:2160"))
        self.cameraLabel.setText(_translate("Touch_Projector_Setting", "主摄像: 顶部摄像:"))
        self.comboMainCamera.setItemText(0, _translate("Touch_Projector_Setting", "0"))
        self.comboMainCamera.setItemText(1, _translate("Touch_Projector_Setting", "1"))
        self.comboMainCamera.setItemText(2, _translate("Touch_Projector_Setting", "2"))
        self.comboTopCamera.setItemText(0, _translate("Touch_Projector_Setting", "0"))
        self.comboTopCamera.setItemText(1, _translate("Touch_Projector_Setting", "1"))
        self.comboTopCamera.setItemText(2, _translate("Touch_Projector_Setting", "2"))
        self.label_show_camera.setText(_translate("Touch_Projector_Setting", "CameraContent"))
        self.slot_init()

    '''Initializes all slot functions'''

    def slot_init(self):
        self.comboMainCamera.setCurrentText(str(self.co_list[6][0]))
        self.comboTopCamera.setCurrentText(str(self.co_list[6][1]))
        self.ButtonOpenCamera.clicked.connect(self.button_open_camera_clicked)
        self.timer_camera.timeout.connect(self.show_camera)  # If the timer ends, call show_camera()
        self.ButtonSaveExit.clicked.connect(self.save_close)
        self.ButtonUp.clicked.connect(self.click_button_up)
        self.ButtonDown.clicked.connect(self.click_button_down)
        self.ButtonLeft.clicked.connect(self.click_button_left)
        self.ButtonRight.clicked.connect(self.click_button_right)
        self.ButtonRefreshResolution.clicked.connect(self.refresh_resolution)
        self.corner_group = QtWidgets.QButtonGroup()
        self.corner_group.addButton(self.LandLeftTopPoint)
        self.corner_group.addButton(self.PortLeftTopPoint)
        self.corner_group.addButton(self.PortRightBottomPoint)
        self.corner_group.addButton(self.LandRightBottomPoint)
        self.corner_group.addButton(self.TouchDivider)
        self.corner_group.setExclusive(True)
        self.corner_group.buttonClicked.connect(self.select_corner_point)
        self.corner_index = -1

    def button_open_camera_clicked(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(int(self.comboCurrCamNum.currentText()))
            if flag == False:  # camera failed to open
                msg = QtWidgets.QMessageBox.warning(self, 'warning', "请检查相机于电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.ButtonOpenCamera.setText('关闭摄像头')
                self.currCamNum.setText('当前摄像头：' + str(self.current_camera_number))
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.ButtonOpenCamera.setText('开启摄像头')
            self.currCamNum.setText('选择摄像头：')

    def show_camera(self):
        flag, self.image = self.cap.read()  # Read from the video stream

        show = cv2.resize(self.image, (640, 480))  # Set the size of the frame to 640x480
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # Video color conversion back to RGB
        self.draw_camera_conners(show, self.co_list)  # Draw the corner indicator of the phone
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # Convert the video data to QImage format
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))  # show QImage in label box

    def save_close(self):
        self.co_list[6] = [self.comboMainCamera.currentText(), self.comboTopCamera.currentText()]
        self.tp_utils.write_csv_data('co.conf', self.co_list)
        self.close()

    def select_corner_point(self):
        corner_id = self.corner_group.checkedId()
        if corner_id == -2:
            self.corner_index = 2
        elif corner_id == -3:
            self.corner_index = 0
        elif corner_id == -4:
            self.corner_index = 1
        elif corner_id == -5:
            self.corner_index = 3
        elif corner_id == -6:
            self.corner_index = 4

    def click_button_up(self):
        if self.co_list[self.corner_index][1] > self.STEP:
            self.co_list[self.corner_index][1] -= self.STEP

    def click_button_down(self):
        if self.co_list[self.corner_index][1] < 480 - self.STEP:
            self.co_list[self.corner_index][1] += self.STEP

    def click_button_left(self):
        if self.co_list[self.corner_index][0] > self.STEP and self.corner_index < 4:
            self.co_list[self.corner_index][0] -= self.STEP

    def click_button_right(self):
        if self.co_list[self.corner_index][0] < 640 - self.STEP and self.corner_index < 4:
            self.co_list[self.corner_index][0] += self.STEP

    def refresh_resolution(self):
        width, height = self.p_opr.get_width_height()
        self.phonePixels.setText("宽:" + str(width) + " 高:" + str(height))
        self.co_list[5] = [width, height]

    def draw_camera_conners(self, capture_frame, coordinates):
        # Show corner locations in portrait
        selected_color = (255, 0, 0)  # RED
        unselected_color = (0, 255, 0)  # GREEN
        cv2.line(capture_frame, (int(coordinates[0][0]), int(coordinates[0][1])),
                 (int(coordinates[0][0]) + 10, int(coordinates[0][1])), selected_color if self.corner_index == 0 else unselected_color, 2)  # LEFT_TOP
        cv2.line(capture_frame, (int(coordinates[0][0]), int(coordinates[0][1])),
                 (int(coordinates[0][0]), int(coordinates[0][1]) + 10), selected_color if self.corner_index == 0 else unselected_color, 2)
        cv2.line(capture_frame, (int(coordinates[1][0]), int(coordinates[1][1])),
                 (int(coordinates[1][0]) - 10, int(coordinates[1][1])), selected_color if self.corner_index == 1 else unselected_color, 2)  # RIGHT_BOTTOM
        cv2.line(capture_frame, (int(coordinates[1][0]), int(coordinates[1][1])),
                 (int(coordinates[1][0]), int(coordinates[1][1]) - 10), selected_color if self.corner_index == 1 else unselected_color, 2)
        # Show corner locations in landscape
        cv2.line(capture_frame, (int(coordinates[2][0]), int(coordinates[2][1])),
                 (int(coordinates[2][0]) + 10, int(coordinates[2][1])), selected_color if self.corner_index == 2 else unselected_color, 2)  # LANDSCAPE_LEFT_TOP
        cv2.line(capture_frame, (int(coordinates[2][0]), int(coordinates[2][1])),
                 (int(coordinates[2][0]), int(coordinates[2][1]) + 10), selected_color if self.corner_index == 2 else unselected_color, 2)
        cv2.line(capture_frame, (int(coordinates[3][0]), int(coordinates[3][1])),
                 (int(coordinates[3][0]) - 10, int(coordinates[3][1])), selected_color if self.corner_index == 3 else unselected_color, 2)  # LANDSCAPE_RIGHT_BOTTEM
        cv2.line(capture_frame, (int(coordinates[3][0]), int(coordinates[3][1])),
                 (int(coordinates[3][0]), int(coordinates[3][1]) - 10), selected_color if self.corner_index == 3 else unselected_color, 2)
        cv2.line(capture_frame, (0, int(coordinates[4][1])), (640, int(coordinates[4][1])), selected_color if self.corner_index == 4 else unselected_color, 1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Touch_Projector_Setting()
    ui.show()
    sys.exit(app.exec_())
