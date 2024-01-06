####### memanggil library PyQt5 ##################################
#----------------------------------------------------------------#
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtQml import * 
from PyQt5.QtWidgets import *
from PyQt5.QtQuick import *  
import sys
import time
import threading
import glob  # Tambahkan import glob

##################################################################
#----------------deklarasi variabel------------------------------#
analog = 110
input1_color = "#df1c39"
input2_color = "#df1c39"

button1_status = "0"
button2_status = "0"
button3_status = "0"

analog_output = "0"

##################################################################
#----------------mengaktifkan komunikasi serial------------------#
import sys
import serial
import threading

serial_data = ""

transmit_time = 0
transmit_time_prev = 0

data_send = ""

print("select your arduino port:")

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

print(str(serial_ports()))

port = input("write port : ")

ser = serial.Serial(port, 9600, timeout=3)


########## mengisi class table dengan instruksi pyqt5#############
#----------------------------------------------------------------#
class table(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app = QApplication(sys.argv)
        self.engine = QQmlApplicationEngine(self)
        self.engine.rootContext().setContextProperty("backend", self)
        self.engine.load(QUrl("main.qml"))
        sys.exit(self.app.exec_())

    ######################KIRIM DATA ANALOG KE GAUGE##############
    @pyqtSlot(result=float)
    def get_analog(self):  
        return analog

    ####################KIRIM DATA WARNA STATUS BUTTON#############
    @pyqtSlot(result=str)
    def get_input1_color(self):  
        return input1_color

    @pyqtSlot(result=str)
    def get_input2_color(self):  
        return input2_color
    
    @pyqtSlot(int, bool)
    def updateParkingSlots(self, index, is_empty):
        # Mengirimkan sinyal ke QML untuk memperbarui warna slot parkir
        if is_empty:
            self.engine.rootObjects()[0].children()[2].children()[index].setProperty("slotColor", "green")
        else:
            self.engine.rootObjects()[0].children()[2].children()[index].setProperty("slotColor", "red")

#----------------------------------------------------------------#
###############################MEMBACA DATA SERIAL##################
def serial_read(num):
    global ser_bytes
    global decoded_bytes
    global serial_data
    global analog
    global data
    global input1_color
    global input2_color

    while True:
        try:
            ser_bytes = ser.readline()
            serial_data = (ser_bytes.decode('utf-8')[:-2])

            print(serial_data)

        except:
            serial_data = serial_data

        # Memastikan bahwa data dimulai dengan 'S' dan sisanya adalah angka
        if serial_data.startswith('S') and serial_data[1:].isdigit():
            data = serial_data.split(":")

            analog = int(data[1])
            # print(analog)
            if (data[2] == "0"):
                input1_color = "#df1c39"
            else:
                input1_color = "#04f8fa"

            if (data[3] == "0"):
                input2_color = "#df1c39"
            else:
                input2_color = "#04f8fa"

            main.updateParkingSlots(0, data[1] == "0")
            main.updateParkingSlots(1, data[2] == "0")
            main.updateParkingSlots(2, data[3] == "0")
            main.updateParkingSlots(3, data[4] == "0")

#----------------------------------------------------------------#

def serial_write(num):
    global transmit_time
    global transmit_time_prev
    global data_send

    while True:
        transmit_time = time.time() - transmit_time_prev
        data_send = (str("*") + str(button1_status) + str("|")
                     + str(button2_status) + str("|")
                     + str(button3_status) + str("|")
                     + str(analog_output) + str("|")
                     )
        if (transmit_time > 0.5):
            # print(data_send)
            ser.write(data_send.encode())
            transmit_time_prev = time.time()


########## memanggil class table di mainloop######################
#----------------------------------------------------------------#
if __name__ == "__main__":
    t1 = threading.Thread(target=serial_read, args=(10,))
    t1.start()

    t2 = threading.Thread(target=serial_write, args=(10,))
    t2.start()

    main = table()