import serial, threading

from pynput.keyboard import Listener as K_Listener

from pynput.mouse import Listener as M_Listener

from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QTextEdit

from PyQt5.QtGui import QPixmap

import cv2

class Window(QMainWindow):

    def __init__(self):

        super().__init__()

        self.ACTIVE_WIDGETS = []

        self.setGeometry(0, 0, 1160, 500)
        self.show()

        self.Generate_Gui()

    def Generate_Gui(self):


        self.SHEET = """
        
        QPushButton#SAFE{
            background-color: green;
        }
        
        QPushButton#ARMED{
            background-color: red;
        }
        
        """

        self.Console_Message_Manager = QTextEdit(self)
        self.Console_Message_Manager_String = "WARNING\n----------------------------------------\nDO NOT POINT AT OR NEAR THE FACE OF ANYONE\nAVOID LOOKING DIRECTLY AT THE LASER OR SURFACES IT MAY REFLECT OFF OF\nPLEASE EXERCISE CAUTION WITH ALL USE\n----------------------------------------\n\n"
        self.Console_Message_Manager_String += "USAGE\n----------------------------------------\nHORIZONTAL AND VERTICAL MOVEMENT IS MANAGED BY THE ARROW KEYS\nTHE LEFT MOUSE KEY, WHEN ARMED, CAN BE USED TO TRIGGER THE LASER\nTHE RIGHT MPISE KEY CAN BE USED TO ARM AND DISARM THE DEVICE\n----------------------------------------\n\n"
        self.Console_Message_Manager_String += "ERROR LOG\n----------------------------------------\n\n"
        self.Console_Message_Manager.setReadOnly(True)

        self.safety_indicator = QPushButton("SAFE", self)
        self.safety_indicator.setGeometry(660, 430, 490, 50)
        self.safety_indicator.setStyleSheet(self.SHEET)
        self.safety_indicator.setObjectName("SAFE")
        self.ACTIVE_WIDGETS.append(self.safety_indicator)

        self.safety = -1

        try:

            self.board = serial.Serial('COM2', 115200)

        except:

            self.Console_Message_Manager_String += "> An error has occurred while initializing communications for this device.\n> > Please make sure you have the device firmly plugged in and attempt a restart.\n"

        try:

            self.VIDEO = cv2.VideoCapture(0)

            self.Optic_Screen = QLabel(self)

            self.Optic_Screen.move(10, 10)

            self.ACTIVE_WIDGETS.append(self.Optic_Screen)

            self.Optic_Thread_Object = threading.Thread(target=self.Optic_Thread)

            self.Optic_Thread_Object.start()

        except:

            self.Console_Message_Manager_String += "> An error has occurred while accessing the optics for this device.\n> > Make sure your optics are firmly plugged in and attempt a restart.\n"

        try:

            self.Keyboard = K_Listener(on_press=self.Key_On_Press)

            self.Keyboard.start()

        except:

            self.Console_Message_Manager_String += "> An error has occurred while initializing your movement control device.\n> > Please make sure you have a keyboard firmly plugged in and attempt a restart.\n"

        try:

            self.Mouse = M_Listener(on_click=self.Mouse_On_Click, on_move=self.Mouse_On_Move)

            self.Mouse.start()

        except:

            self.Console_Message_Manager_String += "> An error has occurred while initializing your turret trigger.\n> > Please make sure you have a mouse firmly plugged in and attempt a restart.\n"

        if len(self.Console_Message_Manager_String) >= 0:

            self.Console_Message_Manager.setText(self.Console_Message_Manager_String)

            self.ACTIVE_WIDGETS.append(self.Console_Message_Manager)

            self.Console_Message_Manager.setGeometry(660, 10, 490, 410)

        self.Show_Widgets()

    def Optic_Thread(self):

        sentinel = 0

        while self.VIDEO.isOpened():

            self.ret, self.frame = self.VIDEO.read()

            cv2.imwrite('frame.jpg', self.frame)

            self.frame = QPixmap('frame.jpg')

            if sentinel == 0:

                self.Optic_Screen.resize(self.frame.width(), self.frame.height())

                sentinel += 1

            self.Optic_Screen.setPixmap(self.frame)

            k = cv2.waitKey(10)

    def Key_On_Press(self, key):

        if str(key) == "Key.left":

            pass

            #self.board.write('L'.encode())

        elif str(key) == "Key.right":

            pass

            #self.board.write('R'.encode())

        elif str(key) == "Key.up":

            pass

            #self.board.write('U'.encode())

        elif str(key) == "Key.down":

            pass

            #self.board.write('D'.encode())

    def Mouse_On_Click(self, x, y, button, pressed):

        if pressed and str(button) == "Button.right":

            self.safety *= -1

            if self.safety == -1:

                self.safety_indicator.setText("SAFE")

                self.safety_indicator.setObjectName("SAFE")

            else:

                self.safety_indicator.setText("ARMED")

                self.safety_indicator.setObjectName("ARMED")

            self.safety_indicator.setStyleSheet(self.SHEET)

        if pressed and str(button) == "Button.left" and self.safety == 1:

            print("fire")

            pass #self.board.write('F'.encode())

        else:

            print("No fire")

            pass #self.board.write('S'.encode())

    def Mouse_On_Move(self, x, y):

        print(x, y)

        #ADD MOVEMENT SO WE CAN REMOVE THE KEY THING

    def Show_Widgets(self):

        for elem in self.ACTIVE_WIDGETS:

            elem.show()

    def Hide_Widgets(self):

        for elem in self.ACTIVE_WIDGETS:

            elem.hide()

def Main():

    app = QApplication([])

    x = Window()

    app.exec_()

Main()