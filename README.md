# raspberrypi-toyproject-2024

**스마트홈**

## 배경
실시간으로 가정의 환경을 모니터링하고 제어할 수 있는 기능을 구현

## 기능
    - LED ON/OFF 기능: 사용자가 LED 조명을 켬/끔 및 조명의 밝기 조절 가능
    - 알람 기능: 원하는 시간에 알람을 설정하고 설정된 시간에 정확하게 알람이 울림
    - 온습도 감지 기능: 온습도 감지 센서를 통해 데이터를 수집하고, 데이터를 UI에 표시하여 온도와 습도를 실시간으로 모니터링 가능

## 특징
- 사용 모듈 : LED, 피에조 부저, 온습도 센서

<img src="https://raw.githubusercontent.com/LEUNSU/raspberrypi-toyproject-2024/main/images/rb013.png" width='300'>

- QtDesigner로 UI 설계 

![UI화면](https://raw.githubusercontent.com/LEUNSU/raspberrypi-toyproject-2024/main/images/rb001.png)

- Raspberry Pi 사용하여 터미널로 프로그램 작동 결과 확인

![작동 결과](https://raw.githubusercontent.com/LEUNSU/raspberrypi-toyproject-2024/main/images/rb004.png)

![작동 결과](https://raw.githubusercontent.com/LEUNSU/raspberrypi-toyproject-2024/main/images/rb006.png)


## 프로그램 실행

**하드웨어**

<img src="https://raw.githubusercontent.com/LEUNSU/raspberrypi-toyproject-2024/main/images/rb010.png" width='300'>

**소프트웨어**

- LED ON/OFF 기능

![LED기능](https://raw.githubusercontent.com/LEUNSU/raspberrypi-toyproject-2024/main/images/rb007.png)
    
    - QSlider를 움직이면서 LED 밝기 조절 

- 알람기능

![알람기능](https://raw.githubusercontent.com/LEUNSU/raspberrypi-toyproject-2024/main/images/rb002.png)

    - 다이얼로 알람이 울릴 시간을 설정, 설정된 시간이 되면 피에조 부저 작동
    - 알람이 울린 후 OFF버튼을 누르면 알람 OFF 및 LED ON, 2초 뒤 OFF

- 온습도 감지 기능

![온습도기능](https://raw.githubusercontent.com/LEUNSU/raspberrypi-toyproject-2024/main/images/rb003.png)






