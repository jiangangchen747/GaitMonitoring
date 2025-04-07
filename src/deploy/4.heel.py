from picamera import PiCamera
import datetime
import time
from time import sleep
from fractions import Fraction
import RPi.GPIO as GPIO
import socket
import numpy as np
import pandas as pd


sudo date -s "20 FEB 2024 21:00:00"

pin_to_circuit = 24
interrupt_pin = 15

UDP_IP_t = "192.168.0.101"
UDP_PORT_t = 6006
Message = b'4.heel'
UDP_IP_r = "192.168.0.104"
UDP_PORT_r = 6001

GPIO.setmode(GPIO.BCM)

def camStart():
    camera = PiCamera(resolution=(1296, 972), 
                      framerate=Fraction(30, 1))
    camera.led = False
    camera.iso = 800
    sleep(2)
    camera.shutter_speed = 3000 
    camera.exposure_mode = 'off'
    sleep(1)
    print('cam start')
    return camera

def get_date():
    data = datetime.datetime.now().strftime("%m_%d_%Y-%H-%M-%S")
    return data

def isoImaging(camera):
    time_1 = time.perf_counter()
    global time_capture
    global numOfStep
    string = str(numOfStep)
    camera.capture("/home/pi4/Desktop/Images/"+ time_capture + "-" + string +".jpg",
                   use_video_port=True, 
                   quality=90)
    time_2 = time.perf_counter()
    print(string + ' Time for Imaging: ', time_2 - time_1)

def fsr_count (pin_to_circuit):
    count = 0
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    sleep(0.1)
    GPIO.setup(pin_to_circuit, GPIO.IN)
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
    return count

def interrupt_func(channel):
    global camera
    global time_pre
    global numOfStep
    global StepData
    time_pre = time.perf_counter()
    sock_send.sendto(Message, (UDP_IP_t, UDP_PORT_t))
    isoImaging(camera)
    numOfStep = numOfStep + 1
    StepData[0,1] = numOfStep

if __name__ == '__main__':
    camera = camStart()
    time_capture = get_date()
    GPIO.setup(interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(interrupt_pin, GPIO.RISING, 
                          callback=interrupt_func, bouncetime=50)
    GaitData = np.zeros((1, 2))
    numOfStep = 0
    time_pre = 0
    stepTime = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP_r, UDP_PORT_r))
    sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            StepData = np.zeros((1, 2))
            print('        wait for UDP interrupt, 4 -> 1 left step time')
            data, addr = sock.recvfrom(1024)
            time_now = time.perf_counter()
            StepData[0,0] = time_now - time_pre
            GaitData = np.vstack([GaitData, StepData])
    except KeyboardInterrupt:
        pass
    finally:
        index_name = [_ for _ in range(0, np.shape(GaitData)[0])]
        column = ['StepTime', '#Step']
        columns_names = [_ for _ in column]
        df = pd.DataFrame(GaitData, index=index_name, columns=columns_names)
        df.to_csv('df-' + time_capture + '.csv', index=True, header=True, sep='|')
        
        GPIO.cleanup()
        camera.close()




