import cv2
import serial
import time
import numpy as np

# ---- Serial ----
arduino = serial.Serial("COM3", 9600, timeout=1)
time.sleep(2)

# ---- Ventana OpenCV ----
cv2.namedWindow("Control Servo (q=salir)", cv2.WINDOW_NORMAL)

img = np.zeros((200, 500, 3), dtype=np.uint8)

print("Teclas:")
print("a = mover 1 vez")
print("e = mover 2 veces")
print("i = mover 3 veces")
print("o = mover 4 veces")
print("u = mover 5 veces")
print("q = salir")

while True:

    cv2.imshow("Control Servo (q=salir)", img)

    k = cv2.waitKey(1) & 0xFF

    if k == ord('a'):
        arduino.write(b'1')
        print("Servo -> 1 vez")

    elif k == ord('e'):
        arduino.write(b'2')
        print("Servo -> 2 veces")

    elif k == ord('i'):
        arduino.write(b'3')
        print("Servo -> 3 veces")

    elif k == ord('o'):
        arduino.write(b'4')
        print("Servo -> 4 veces")

    elif k == ord('u'):
        arduino.write(b'5')
        print("Servo -> 5 veces")

    elif k == ord('q'):
        break

arduino.close()
cv2.destroyAllWindows()