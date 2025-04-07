from picamera import PiCamera
import datetime
from time import sleep
from fractions import Fraction


def camStart():
    camera = PiCamera(resolution=(1296, 972), 
                      framerate=Fraction(30, 1))
    camera.led = False
    print('cam start')
    return camera

def originImage(camera):
    sleep(2)
    time_1 = datetime.datetime.now()
    camera.capture('/home/pi3/Desktop/Images/originImage.jpg')
    time_2 = datetime.datetime.now()
    diff = time_2 - time_1
    diff_in_s = diff.total_seconds()

def isoImage(camera):
    camera.iso = 800
    sleep(2)
    camera.shutter_speed = 20000 
    camera.exposure_mode = 'off'
    # camera.exposure_compensation = 12
    # camera.brightness = 60
    # camera.contrast = 50
    # camera.framerate = 90
    # g = camera.awb_gains
    # camera.awb_mode = 'off'
    # camera.awb_gains = g
    sleep(1)
    time_1 = datetime.datetime.now()
    camera.capture('/home/pi3/Desktop/Images/isoImage.jpg', 
                   use_video_port=True, 
                   quality=90)
    time_2 = datetime.datetime.now()
    diff = time_2 - time_1
    diff_in_s = diff.total_seconds()

if __name__ == '__main__':
    camera = camStart()
    try:
        originImage(camera)
        isoImage(camera)
        pass
    finally:
        camera.close()




