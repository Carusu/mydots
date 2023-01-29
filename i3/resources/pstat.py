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
    def __init__(self, pstat, color_header, color_line1, color_lines23, bg_color, font, font_size, offset):
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
        
        self.cmd = 'ps -eo comm,pid,' + pstat + ' --sort -' + pstat + ' | grep -v pstat.py | head -4'
        self.proc = subprocess.Popen([self.cmd], stdout=subprocess.PIPE, shell=True)
        (self.out, self.err) = self.proc.communicate()
        self.headerTxt = self.out.decode("utf-8").split("\n")[0]
        self.line1Txt  = self.out.decode("utf-8").split("\n")[1]
        self.line2Txt  = self.out.decode("utf-8").split("\n")[2]
        self.line3Txt  = self.out.decode("utf-8").split("\n")[3]

        # Create the label and set its text
        self.header = QLabel(self.headerTxt)
        self.header.setStyleSheet(f"color: {color_header}")
        self.line1 = QLabel(self.line1Txt)
        self.line1.setStyleSheet(f"color: {color_line1}")
        self.line2 = QLabel(self.line2Txt)
        self.line2.setStyleSheet(f"color: {color_lines23}")
        self.line3 = QLabel(self.line3Txt)
        self.line3.setStyleSheet(f"color: {color_lines23}")
        
        # Add the label to the layout
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.line1)
        self.layout.addWidget(self.line2)
        self.layout.addWidget(self.line3)
        
                # Set the window size and show it
        self.setLayout(self.layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.command_updater)
        self.timer.start(MS_DELAY)
        self.installEventFilter(self)
        self.show()

        
        
    def command_updater(self):
      cmd = 'ps -eo comm,pid,' + pstat + ' --sort -' + pstat + ' | grep -v pstat.py | head -4'
      proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
      (out, err) = proc.communicate()
      headerTxt = out.decode("utf-8").split("\n")[0]
      line1Txt  = out.decode("utf-8").split("\n")[1]
      line2Txt  = out.decode("utf-8").split("\n")[2]
      line3Txt  = out.decode("utf-8").split("\n")[3]
      self.header.setText(headerTxt)
      self.line1.setText(line1Txt)
      self.line2.setText(line2Txt)
      self.line3.setText(line3Txt)
      
    def eventFilter(self, object, event):
      if event.type() == QEvent.Type.WindowDeactivate:
        self.close()
      return 0



if __name__ == "__main__":
    setproctitle.setproctitle(sys.argv[0].split("/")[-1])
    pstat = sys.argv[1]
    color_header  = '#8FC2F6'
    color_line1   = '#fff68c'
    color_lines23 = 'white' 
    bg_color      = '#4f4b5e'

    font = "Ubuntu Mono"
    font_size = 11
    if pstat == 'pmem':
        offset = (1425, 22)
    elif pstat == 'pcpu':
        offset = (1475, 22)
    
    app = QApplication(sys.argv)
    win = Main(pstat, color_header, color_line1, color_lines23, bg_color, font, font_size, offset)
    sys.exit(app.exec())
