from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def button_min_pressed():
    ret, frame = cap.read()
    print(np.min(frame))

def button_max_pressed():
    ret, frame = cap.read()
    print(np.max(frame))

def button_pressed():
    print('pressed')

app = QApplication([])
win = QMainWindow()

central_widget = QWidget()

button1 = QPushButton('Test', central_widget)
button1.setGeometry(0,50,120,40)
button1.clicked.connect(button_pressed)

button2 = QPushButton('Second', central_widget)
button2.setGeometry(0,90,120,40)

button_min = QPushButton('Min', central_widget)
button_max = QPushButton('Max', central_widget)
button_min.clicked.connect(button_min_pressed)
button_max.clicked.connect(button_max_pressed)

layout = QVBoxLayout(central_widget)
layout.addWidget(button_min)
layout.addWidget(button_max)
layout.addWidget(button2)
layout.addWidget(button1)

win.setCentralWidget(central_widget)
win.setGeometry(0, 0, 200, 200)

win.show()
app.exit(app.exec_())
cap.release()
