import RPi.GPIO as GPIO
import time
#import bluetooth
# Allow Bluetooth Connection
#server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
#port = 1
#server_sock.bind(("",port))
#server_sock.listen(1)
#client_sock,address = server_sock.accept()
#print("Accepted connection from ",address)

#while True:
#    recvdata = client_sock.recv(1024)
#    print("Received \"%s\" through Bluetooth" % recvdata)
#    if (recvdata == "Q"):
#        print ("Exiting")
#        break
#client_sock.close()
#server_sock.close()


# Set variables for Motor pins and camera focus/shutter
in1 = 26
in2 = 20
in3 = 16
in4 = 19
temp1=1

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
print("1-auto_program r-run s-stop f-forward b-backward p-picture e-exit")
print("\n")



while(1):

    #x=client_sock.recv(1024)
    x=raw_input()

    if x=='c':
        def take_picture():
            print("focusing")
            GPIO.output(in3,GPIO.LOW)
            time.sleep(.75)
            print("taking picture")
            GPIO.output(in4,GPIO.LOW)
            time.sleep(.75)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.HIGH)
        def move_forward():
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            temp1=1
        def move_backward():
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            temp1=0
        def stop():
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
        mvinterval = input("Number of Pictures: ")
        mvduration = input("Motor on Duration (in seconds): ")
        mvpause = input("Pause Between Pictures: ")
        mvdirection = raw_input("(f)orward or (b)ackward: ")
        print("Starting Program")
        for i in range(mvinterval):
            if mvdirection =='f':
                time.sleep(1)
                take_picture()
                time.sleep(1)
                move_forward()
                time.sleep(mvduration)
                stop()
                time.sleep(mvpause)
            if mvdirection =='b':
                time.sleep(1)
                take_picture()
                time.sleep(1)
                move_backward()
                time.sleep(mvduration)
                stop()
                time.sleep(mvpause)
        x='s'

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

    elif x=='e':
        GPIO.cleanup()
        break

    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")

#client_sock.close()
#server.sock.close()
