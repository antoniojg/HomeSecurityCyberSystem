#Antonio Garcia & Jake
import time
import RPi.GPIO as GPIO
import smtplib
import picamera
import datetime as dt
from bottle import route, run, template
from threading import Thread

GMAIL_USER = 'userID@gmail.com' # replace "userID" with a valid gmail user ID
GMAIL_PASS = 'mypassword'       # replace "mypassword" with the user's password
                                # ASK YOUR GROUP PARTNERS TO NOT LOOK!
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

button_pressed = False
motion_detected = 0

BUZZER_PIN = 10
BUTTON_PIN = 18
SENSOR_PIN = 11

GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_callback():
    global button_pressed
    button_pressed = True

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback)

GPIO.setup(SENSOR_PIN, GPIO.IN)

def check_motion():
    print("Checking for motion")
    while True:
        time.sleep(0.1)
        motion_detected = GPIO.input(SENSOR_PIN)
        if motion_detected == 1:
    		#motion detected
            print('Motion detected')
            start_buzz_timer()
            time.sleep(5)
            break

def send_email(recipient, subject, text):
    smtpserver = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(GMAIL_USER, GMAIL_PASS)
    header = 'To:' + recipient + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject:' + subject + '\n'
    msg = header + '\n' + text + ' \n\n'
    smtpserver.sendmail(GMAIL_USER, recipient, msg)
    smtpserver.close()

def reset_vars():
    global motion_detected
    global button_pressed
    motion_detected = 0
    button_pressed = 0

def intruder_detected ():
    take_picture()
    send_email()
    reset_vars()

def take_picture ():
    name = str(dt.datetime.now()) + '.jpg'
    camera = picamera.PiCamera()
    camera.capture(name)

def buzz(pitch, duration):
    '''controller function for buzzer'''
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
    	GPIO.output(BUZZER_PIN, True)
    	time.sleep(delay)
    	GPIO.output(BUZZER_PIN, False)
    	time.sleep(delay)

def start_buzz_timer (duration) :
    '''starts a buzzer timer that's able to be interrupted by a button press - if not pressed, calls intruder_detected'''
    time_between = .8 #seconds
    global button_pressed
    button_pressed = False
    while not button_pressed:
        for speed_step in range(4):
            for buzzes in range(4):
                buzz(1000, .25)
                time.sleep(time_between)
            time_between = time_between / 2
    if (not button_pressed):
        print('Button not presed in time - calling intruder_detected')
        intruder_detected()

if __name__ == '__main__':
    try:
        check_motion()
    finally:
        GPIO.cleanup()
