import cv2
import numpy as np
import serial
import time
import threading

def send_data(x):
    ardu= serial.Serial('COM7',9600, timeout=.1)
    #print("sending alert")
    ardu.write(x.encode())
    ardu.close()

def human_detection():
    # Load YOLO
    net = cv2.dnn.readNet("person.weights", "person.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # Initialize variables
    prev_detection = True  # Set to True initially to ensure sending 2 at the beginning
    last_detection_time = time.time()

    # Initialize video capture
    cap = cv2.VideoCapture(0)  # 0 represents the default camera, change it if you have multiple cameras

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width, channels = frame.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing information on the screen
        class_ids = []
        confidences = []
        boxes = []

        human_detected = False  # Reset the human detection status for each frame

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected is a person
                    if class_id == 0:
                        human_detected = True
                        last_detection_time = time.time()
                        break

        # Send data via serial port only if human detection status changes
        if human_detected != prev_detection:
            if human_detected:
                #print('sending 1')
                x = '1'
                send_data(x)
            else:
                last_detection_time = time.time()
                #print('No human detected')

        # If human is not detected for 5 seconds, send '2' signal
        if not human_detected and time.time() - last_detection_time >= 5:
            #print('sending 2')
            y = '2'
            send_data(y)

        # Update previous detection status
        prev_detection = human_detected

        # Display the frame
        cv2.imshow('Human Detection', frame)

        # Check for key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and close serial port
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    pass
    #threading.Thread(target=human_detection).start()