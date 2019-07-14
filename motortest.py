from bluetooth import *
import RPi.GPIO as GPIO
from threading import Timer, Thread, Event
from datetime import datetime
from math import floor
import time


server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)
uuid = "94f39d29-8d6d-437d-973b-fba39e49d4ee"
port = server_sock.getsockname()[1]

advertise_service( server_sock, "BTS",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ],
                    )

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)


in1 = 26
in2 = 20
in3 = 16
in4 = 19
temp1=1

motorTime = 0
motorDuration = 0
moving = false
picDelay = 0
lastPic = 0
lastMove = 0
direction = 'f'

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.HIGH)
GPIO.output(in4,GPIO.HIGH)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")

# Timer that is called every n seconds to "update" the screen
class perpetualTimer():
   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def timeEvent():
    move = floor((datetime.now().timestamp() - float(lastMove)) / 60)
    pic = floor((datetime.now().timestamp() - float(lastPic)) / 60)
    if move >= motorTime:
        print('motorDuration' + motorTime)
        print('motorDuration' + motorDuration)
        if direction == 'f':
            forward()
        else:
            backward()
        if move >= move + motorDuration:
            print('update last move' + move)
            lastMove = move
    if pic >= picDelay:
        lastPic = pic
        takePicture()

def forward():
    print("forward")
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    temp1=1

def backward():
    print("backward")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    temp1=0

def takePicture():
    print("focusing")
    GPIO.output(in3,GPIO.LOW)
    time.sleep(.5)
    print("taking picture")
    GPIO.output(in4,GPIO.LOW)
    time.sleep(.5)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.HIGH)

while(1):

    x=client_sock.recv(1024)

    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         x='z'

    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='p':
        print("focusing")
        GPIO.output(in3,GPIO.LOW)
        time.sleep(.5)
        print("taking picture")
        GPIO.output(in4,GPIO.LOW)
        time.sleep(.5)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.HIGH)
    # string format === 't,direction = f || d, motorTime, picDelay, motorDuration'
    elif x[0]=='t':
        print('Run Full Gammut')
        letters = x.split(',');
        digits =  [x for x in letters if type(x)==int ]
        direction = letters[1]
        motorTime = digits[0]
        picDelay = digits[1]
        motorDuration = digits[2]
        screen_update_timer = perpetualTimer(5, timeEvent)
        screen_update_timer.start()
        x = 'z'
    elif x=='e':
        GPIO.cleanup()
        break

    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")

print("Disconnected")

client_sock.close()
server_sock.close()
print("All Closed")
