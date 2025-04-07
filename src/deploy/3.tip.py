from picamera import PiCamera
import datetime
import time
from time import sleep
from fractions import Fraction
import RPi.GPIO as GPIO
import threading
import numpy as np
import pandas as pd


sudo date -s "20 FEB 2024 21:00:00"

pin_to_circuit = 24
interrupt_pin = 14

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
    camera.capture("/home/pi3/Desktop/Images/"+ time_capture + "-" + string +".jpg",
                   use_video_port=True, 
                   quality=90)
    time_2 = time.perf_counter()
    print('Time for Imaging: ', time_2 - time_1)

def fsr_count (pin_to_circuit, time_now, time_lift, standing_time):
    count = 0
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    sleep(0.1)
    GPIO.setup(pin_to_circuit, GPIO.IN)
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
        if count == 100:
            time_lift = time.perf_counter()
    return count, time_lift, standing_time

def cadenceThre():
    threading.Timer(60, cadenceThre).start()
    cadence.append(numOfStep)

if __name__ == '__main__':
    camera = camStart()
    time_capture = get_date()

    GPIO.setup(interrupt_pin, GPIO.OUT)
    GPIO.output(interrupt_pin, GPIO.LOW)
    GaitData = np.zeros((1, 5))
    numOfStep = 0
    cadence = []
    cadenceThre()
    strideTime = []
    time_pre = time.perf_counter()
    time_now = time.perf_counter()
    standing_time = 0
    time_lift = time.perf_counter()
    time_lift_true = time.perf_counter()
    swing_time = 0
    single_support_time = swing_time
    
    try:
        count_pre = 1000
        while True:
            StepData = np.zeros((1, 5))
            count, time_lift, standing_time = fsr_count(pin_to_circuit, time_now, time_lift, standing_time)
            print('   FSR reading: ', count)
            if count > 30 and count_pre <= 20:
                time_lift_true = time_lift
            if count <= 20 and count_pre > 30 :
                StepData[0,0] = time_lift_true - time_now
                time_now = time.perf_counter()
                StepData[0,1] = time_now - time_pre
                StepData[0,2] = time_now - time_lift_true
                StepData[0,3] = StepData[0,2]
                GPIO.output(interrupt_pin, GPIO.HIGH)
                isoImaging(camera)
                GPIO.output(interrupt_pin, GPIO.LOW)
                numOfStep = numOfStep + 1
                StepData[0,4] = numOfStep
                count_pre = count
                time_pre = time_now
                GaitData = np.vstack([GaitData, StepData])
            else:
                count_pre = count
    except KeyboardInterrupt:
        pass
    finally:
        index_name = [_ for _ in range(0, np.shape(GaitData)[0])]
        column = ['StandingTime', 'StrideTime', 'SwingTime', 'OtherFootSingleSupportTime', 
                  '#Step']
        columns_names = [_ for _ in column]
        df = pd.DataFrame(GaitData, index=index_name, columns=columns_names)
        df.to_csv('df-' + time_capture + '.csv', index=True, header=True, sep='|')

        GPIO.cleanup()
        camera.close()




