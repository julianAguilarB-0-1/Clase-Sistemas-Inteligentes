import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la camara")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar el frame")
        break

    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gris = cv2.GaussianBlur(gris, (7, 7), 0)
    _, binaria1 = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, binaria2 = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contornos1, _ = cv2.findContours(binaria1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    h, w = binaria1.shape

  
    fondo_azul = np.zeros((h, w, 3), dtype=np.uint8)
    fondo_azul[:] = (0, 255, 0)

   
    for cnt in contornos1:
        area = cv2.contourArea(cnt)

        if area > 1000:  
            
            cv2.drawContours(fondo_azul, [cnt], -1, (0, 0, 255), 2)
        else:
       
            cv2.drawContours(fondo_azul, [cnt], -1, (255,0, 255), 2)

    #cv2.imshow("Dalmata", binaria1)
    cv2.imshow("Maldata", binaria2)
    cv2.imshow("Fondo Rojo", fondo_azul)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()