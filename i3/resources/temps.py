#!/bin/python

import subprocess
import sys
import time
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import setproctitle

MS_DELAY = 1000  # Milliseconds between updates.

class Main(QWidget):
    def __init__(self, color_header, color_line1, color_lines23, bg_color, font, font_size, offset):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        """
        Setting the fonts and the window size, title and properties
        """
        self.window().setFont(QFont(font, font_size))
        self.move(*offset)
        QApplication.instance().setFont(QFont(font, font_size))
        self.setWindowTitle('PyQtwidget')
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {bg_color};")
        
        self.layout = QVBoxLayout()
        
        self.cmd = 'sensors'
        self.proc = subprocess.Popen([self.cmd], stdout=subprocess.PIPE, shell=True)
        (self.out, self.err) = self.proc.communicate()
        self.tempCpu = self.out.decode("utf-8").split("\n")[35].split()[1].replace('+', '')
        #self.tempCpuCrit = '90.0°C'
        self.tempCpuCrit = self.out.decode("utf-8").split("\n")[35].split()[4].replace('+', '').replace(',','')
        self.tempGpu = self.out.decode("utf-8").split("\n")[2].split()[1].replace('+', '')
        #self.tempGpuCrit = self.out.decode("utf-8").split("\n")[4].split()[4].replace('+', '').replace(',','')
        self.tempGpuCrit = '90.0°C'

        # Create the label and set its text
        self.cpuLine = QLabel('CPU temp: ' + self.tempCpu + ' (crit: ' + self.tempCpuCrit + ')')
        self.cpuLine.setStyleSheet(f"color: {color_header}")
        self.gpuLine = QLabel('GPU temp: ' + self.tempGpu + ' (crit: ' + self.tempGpuCrit + ')')
        self.gpuLine.setStyleSheet(f"color: {color_header}")

        # Add the label to the layout
        self.layout.addWidget(self.cpuLine)
        self.layout.addWidget(self.gpuLine)
        
        # Set the window size and show it
        self.setLayout(self.layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.command_updater)
        self.timer.start(MS_DELAY)
        self.installEventFilter(self)
        self.show()

        
        
    def command_updater(self):
      cmd = 'sensors'
      proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
      (out, err) = proc.communicate()
      tempCpu = out.decode("utf-8").split("\n")[35].split()[1].replace('+', '')
      tempCpuCrit = out.decode("utf-8").split("\n")[35].split()[4].replace('+', '').replace(',','')
      tempGpu = out.decode("utf-8").split("\n")[2].split()[1].replace('+', '')
      tempGpuCrit = '90.0°C'
      
      self.cpuLine.setText('CPU temp: ' + tempCpu + ' (crit: ' + tempCpuCrit + ')')
      self.gpuLine.setText('GPU temp: ' + tempGpu + ' (crit: ' + tempGpuCrit + ')')

      
    def eventFilter(self, object, event):
      if event.type() == QEvent.Type.WindowDeactivate:
        self.close()
      return 0



if __name__ == "__main__":
    setproctitle.setproctitle(sys.argv[0])
    color_header  = '#8FC2F6'
    color_line1   = '#fff68c'
    color_lines23 = 'white' 
    bg_color      = '#4f4b5e'
    offset = (1350,22)

    font = "Ubuntu Mono"
    font_size = 11
    
    app = QApplication(sys.argv)
    win = Main(color_header, color_line1, color_lines23, bg_color, font, font_size, offset)
    sys.exit(app.exec())
