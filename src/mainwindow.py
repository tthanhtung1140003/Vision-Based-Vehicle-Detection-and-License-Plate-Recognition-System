########################### Using image ##############################################
# import sys
# import cv2
# from PySide6.QtWidgets import QGraphicsScene, QApplication, QMainWindow
# from PySide6.QtGui import QPixmap, QFont
# from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

# from plate_detect import plate_process
# from image_converter import convert_image_to_pixmap
# from resize import resize_image
# from ui_form import Ui_MainWindow

# class MainWindow(QMainWindow):
#     def send_command_to_arduino(self, command):
#         if self.serial_port.isOpen():
#             self.serial_port.write(command.encode())  # Gửi lệnh đến Arduino
#             print(f"Sent command: {command}")
#             # Đọc phản hồi từ Arduino
#             response = self.serial_port.readAll().data().decode()
#             print(f"Response from Arduino: {response}")
#         else:
#             print("Serial port is not open.")
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)

#         # Set up the serial port for Arduino communication
#         self.serial_port = QSerialPort(self)
#         self.serial_port.setPortName("COM8")  # Replace with your Arduino's port name
#         self.serial_port.setBaudRate(9600)     # Match Arduino's baud rate

#         if not self.serial_port.open(QSerialPort.WriteOnly):
#             print("Unable to open serial port.")
#             sys.exit()

#         img_path = r"...."
#         input_img = cv2.imread(img_path)
#         input_img = resize_image(input_img, 780)

#         output_image, output_licensePlate, output_text = plate_process(input_img)
#         ui_output = convert_image_to_pixmap(output_image)

#         output_licensePlate = resize_image(output_licensePlate, 480)

#         # Convert output images from OpenCV to QPixmap
#         ui_input = convert_image_to_pixmap(input_img)
#         ui_license_plate = convert_image_to_pixmap(output_licensePlate)

#         # Create QGraphicsScene for graphicsView
#         self.scene1 = QGraphicsScene(self)
#         self.ui.graphicsView.setScene(self.scene1)
#         # Add input image to scene1
#         self.scene1.addPixmap(ui_input)

#         # Create QGraphicsScene for graphicsView2
#         self.scene2 = QGraphicsScene(self)
#         self.ui.graphicsView_2.setScene(self.scene2)
#         # Add license plate image to scene2
#         self.scene2.addPixmap(ui_license_plate)

#         # Set the recognized text into the label
#         self.ui.label_2.setText(output_text)
#         font = QFont("Arial", 30)  # Set font to Arial size 30
#         self.ui.label_2.setFont(font)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     widget = MainWindow()
#     widget.show()
#     sys.exit(app.exec())

################################### using video and RFID ###################################

import sys
import cv2
import time
from PySide6.QtWidgets import QGraphicsScene, QApplication, QMainWindow
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import QTimer
from PySide6.QtSerialPort import QSerialPort
from plate_detect import plate_process
from image_converter import convert_image_to_pixmap
from resize import resize_image
from ui_form import Ui_MainWindow
from checkID import check_rfid_plate

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.serial_port = QSerialPort(self)
        self.serial_port.setPortName("COM8")  
        self.serial_port.setBaudRate(9600)

        if not self.serial_port.open(QSerialPort.ReadOnly):
            print("Unable to open serial port.")
            sys.exit()

        self.serial_port.readyRead.connect(self.read_serial_data)
        self.buffer = ""  

        video_path = r"...." 
        self.cap = cv2.VideoCapture(video_path) # 0 if using webcam
        if not self.cap.isOpened():
            print("Unable to open video file.")
            sys.exit()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(24)  

        self.is_video_paused = False  

        self.scene1 = QGraphicsScene(self)
        self.ui.graphicsView.setScene(self.scene1)

        self.scene2 = QGraphicsScene(self)
        self.ui.graphicsView_2.setScene(self.scene2)

        self.scene3 = QGraphicsScene(self)
        self.ui.graphicsView_3.setScene(self.scene3)

        self.scene4 = QGraphicsScene(self)
        self.ui.graphicsView_4.setScene(self.scene4)

        self.ui.button.clicked.connect(self.send_a_command)
    def send_a_command(self):
        self.send_command_to_arduino('A')

    def update_frame(self):
        if not self.is_video_paused:  
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame  
                ui_frame = convert_image_to_pixmap(frame)
                self.scene1.clear()
                self.scene1.addPixmap(ui_frame)
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def read_serial_data(self):
        data = self.serial_port.readAll()
        if data:
            self.buffer += bytes(data).decode('utf-8')
            if '\n' in self.buffer: 
                lines = self.buffer.split('\n')
                for line in lines[:-1]:  
                    self.process_serial_message(line.strip())
                self.buffer = lines[-1]  

    def send_command_to_arduino(self, command):
        if self.serial_port.isOpen():
            self.serial_port.write(command.encode())  
            print(f"Sent command: {command}")
            time.sleep(1)  
            response = self.serial_port.readAll().data().decode()
            print(f"Response from Arduino: {response}")
        else:
            print("Serial port is not open.")

    def process_serial_message(self, message):
        if message.startswith("ID:"):  
            self.ID = message.split("ID:")[1].strip()  
            print(f"ID saved: {self.ID}")  
            self.process_frame()  
        else:
            print(f"Unhandled message: {message}")  

    def process_frame(self):
        if not hasattr(self, 'current_frame'):
            print("No current frame to process.")
            return

        self.is_video_paused = True
        self.timer.stop()

        input_img = resize_image(self.current_frame, 780)
        output_image, output_licensePlate, output_text = plate_process(input_img)

        if output_image is None or output_image.size == 0:
            print("Unable to process image, please check the license plate.")
            self.ui.label_2.setText("No license plate detected.")
            self.is_video_paused = False
            self.timer.start(24) 
            return

        ui_output = convert_image_to_pixmap(output_image)
        ui_license_plate = convert_image_to_pixmap(resize_image(output_licensePlate, 480))

        self.scene1.clear()
        self.scene1.addPixmap(ui_output)

        self.scene2.clear()
        self.scene2.addPixmap(ui_license_plate)

        self.ui.label_2.setText(output_text)
        font = QFont("Arial", 30)
        self.ui.label_2.setFont(font)

        # Check RFID ID against the license plate
        file_path = r"data.txt"  
        result = check_rfid_plate(self.ID, output_text, file_path)
        ok_image_path = r"Icon\ok.png"
        not_ok_image_path = r"Icon\notok.png"

        if result == 1:  
            pixmap_ok = QPixmap(ok_image_path)  

            print ('datasent A')
            if not pixmap_ok.isNull():
                self.scene3.addPixmap(pixmap_ok) 
                self.ui.graphicsView_3.setScene(self.scene3)  
                self.ui.graphicsView_4.setScene(QGraphicsScene())  

            else:
                print("Không thể mở ảnh OK.")

        else:  
            pixmap_not_ok = QPixmap(not_ok_image_path)  
            if not pixmap_not_ok.isNull():
                self.scene4.addPixmap(pixmap_not_ok)  
                self.ui.graphicsView_4.setScene(self.scene4) 
                self.ui.graphicsView_3.setScene(QGraphicsScene())  
            else:
                print("Không thể mở ảnh Not OK.")
        self.is_video_paused = False
        self.timer.start(24)


    def closeEvent(self, event):
        self.cap.release()
        self.serial_port.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())


