import serial
while True:
    x = input("enter :")
    ardu= serial.Serial('COM7',9600, timeout=.1)
    print("sending alert")
    ardu.write(x.encode())
    ardu.close()