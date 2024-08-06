from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import sys
import RPi.GPIO as GPIO
import time
import adafruit_dht
import board

red_pin = 21
blue_pin = 20
piezoPin = 26
sensor_pin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
GPIO.setup(piezoPin, GPIO.OUT)
GPIO.setup(sensor_pin, GPIO.IN)

Buzz = GPIO.PWM(piezoPin, 440)
red_pwm = GPIO.PWM(red_pin, 1000)  # PWM 생성, 주파수 1kHz
red_pwm.start(0)  # 초기 듀티사이클 0

log_num = 0

form_class = uic.loadUiType("./qt.ui")[0]
form_class2 = uic.loadUiType("./MyClock.ui")[0]
form_class3 = uic.loadUiType("./SensorWidget.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 초기 상태 설정
        self.set_initial_led_state()

        # LED
        self.Btn_1.clicked.connect(self.btn01)
        self.Btn_2.clicked.connect(self.btn02)
        self.horizontalSlider.valueChanged.connect(self.change_brightness)  # QSlider 신호 연결

        # ALARM
        self.Btn_5.clicked.connect(self.btn05)
        self.Btn_6.clicked.connect(self.btn06)

        # Temperature, Humidity
        self.Btn_7.clicked.connect(self.btn07)
        self.Btn_8.clicked.connect(self.btn08)

        self.sensor_widget = None
        self.clock_widget = None 

    def set_initial_led_state(self):
        GPIO.output(red_pin, True)  # 빨간 LED 켜짐
        GPIO.output(blue_pin, True)  # 파란 LED 켜짐

    # LED
    def btn01(self):
        red_pwm.ChangeDutyCycle(0)  # 최대 밝기
        print("LED ON")

    def btn02(self):
        red_pwm.ChangeDutyCycle(100)  # 최소 밝기 (LED 꺼짐)
        print("LED OFF")

    def change_brightness(self, value):
        reversed_value = 100 - value  # 값 반전
        red_pwm.ChangeDutyCycle(reversed_value)
        print(f"Brightness: {value} (Reversed: {reversed_value})")

    # ALARM
    def btn05(self):
        self.clock_widget = MyClock()
        self.clock_widget.show()
        GPIO.setup(sensor_pin, GPIO.IN)

    def btn06(self):
        Buzz.stop()
        GPIO.output(blue_pin, False)  # 파란 불 끄기
        print("Alarm OFF")
        QtCore.QTimer.singleShot(2000, self.reset_led_state)  # 2초 후 LED 상태 복구

    def reset_led_state(self):
        # 초기 상태로 LED 복구
        self.set_initial_led_state()
        
    # Temperature, Humidity
    def btn07(self):
        self.sensor_widget = SensorWidget()
        self.sensor_widget.show()
        self.increment_log_num()

    def btn08(self):
        if self.sensor_widget is not None:
            self.sensor_widget.update_timer.stop()
            self.sensor_widget.close()
            self.sensor_widget = None
            GPIO.cleanup(sensor_pin)

    def show_sensor_widget(self):
        if self.sensor_widget is None:
            self.sensor_widget = SensorWidget()
            self.sensor_widget.show()

    def increment_log_num(self):
        global log_num
        log_num += 1

class MyClock(QWidget, form_class2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(400, 500)
        
        self.CurrLcd = self.findChild(QLCDNumber, 'CurrLcd')
        self.dial = self.findChild(QDial, 'dial')
        self.MinLabel = self.findChild(QLabel, 'MinLabel')
        self.timeEdit = self.findChild(QTimeEdit, 'timeEdit')

        self.dial.setMinimum(1)
        self.dial.setMaximum(60)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)
        self.show_time()

        self.dial.valueChanged.connect(self.update_label)
        self.timeEdit.timeChanged.connect(self.update_timeedit)


    def show_time(self):
        current_time = QtCore.QTime.currentTime()
        self.currentTime = current_time.toString('HH:mm:ss')

        if self.CurrLcd is not None: 
            self.CurrLcd.display(self.currentTime)
            
        self.activate_alarm()

    def update_label(self, value):
        self.MinLabel.setText(f"{value}")
        self.update_timeedit()

    def update_timeedit(self):
        dial_value = self.dial.value()
        current_time = QtCore.QTime.currentTime()
        alarm_time = current_time.addSecs(dial_value * 60)
        self.timeEdit.setTime(alarm_time)

    def activate_alarm(self):
        current_time = QtCore.QTime.currentTime()
        alarm_time = self.timeEdit.time()
        
        current_time_str = current_time.toString('HH:mm:ss')
        alarm_time_str = alarm_time.toString('HH:mm:ss')

        if current_time_str == alarm_time_str:
            GPIO.output(blue_pin, True)
            Buzz.start(50)
            print("Alarm ON")

    def closeEvent(self, event):
        Buzz.stop()
        GPIO.output(blue_pin, False)
        GPIO.cleanup()
        event.accept()
        print("Alarm OFF")

class SensorWidget(QWidget, form_class3):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        GPIO.setup(sensor_pin, GPIO.IN)
        self.lcdTemp = self.findChild(QLCDNumber, 'lcdTemp')
        self.lcdHumid = self.findChild(QLCDNumber, 'lcdHumid')
        self.dhtDevice = adafruit_dht.DHT11(board.D22)
        self.update_timer = QtCore.QTimer(self)
        self.update_timer.timeout.connect(self.update_sensor_values)
        self.update_timer.start(2000)
        
        GPIO.setup(sensor_pin, GPIO.IN)

    def update_sensor_values(self):
        try:
            temp = self.dhtDevice.temperature
            humid = self.dhtDevice.humidity
            if temp is not None and humid is not None:
                self.lcdTemp.display(temp)
                self.lcdHumid.display(humid)
                print(f'{log_num} - Temp : {temp}C / Humid : {humid}%')
            else:
                self.lcdTemp.display(0)
                self.lcdHumid.display(0)
        except RuntimeError as ex:
            print(ex.args[0])

    def closeEvent(self, event):
        self.update_timer.stop()
        self.dhtDevice.exit()
        event.accept()  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
