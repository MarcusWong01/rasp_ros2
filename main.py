import sender
import receiver
import webCam
import threading

def webcam_mode():
    while True:
        footage = webCam.capture()
        #sender.sender_socket(footage)

def picamera_mode():
    while True:
        footage = receiver.predict()
        sender.sender_socket(footage)

def main():
    while True:
        print("Welcome ROINAS Server, please select mode below")
        mode = int(input("1. Webcam | 2. PiCamera: "))
        if mode == 1:
            #threading.Thread(target=webcam_mode).start()
            webcam_mode()
        elif mode == 2:
            print("Not available")
            #threading.Thread(target=picamera_mode).start()
        else:
            print("Invalid input")

if __name__ == "__main__":
    main()






