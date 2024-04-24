import receiver
import webCam

def main():
    while True:
        #print("Welcome ROINAS Server, please select mode below")
        mode = 2
        #mode = int(input("1. Webcam | 2. PiCamera: "))
        if mode == 1:
            webCam.capture()
        elif mode == 2:
            receiver.receive_image_process()
        else:
            print("Invalid input")

if __name__ == "__main__":
    main()
