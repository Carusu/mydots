#!/bin/python

import sys
import distro
from PIL import Image
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import time
import subprocess

"""
autoupdate bar, from https://www.pythonguis.com/faq/updating-progressbar-from-qrunner/
"""
class WorkerSignals(QObject):
  progress = pyqtSignal(int)
    
class JobRunner(QRunnable):
  signals = WorkerSignals()
  def __init__(self):
    super().__init__()
  @pyqtSlot()
  def run(self):
    for n in range(100):
      self.signals.progress.emit(n + 1)
      time.sleep(0.025)

class FullScreen(QWidget):
  def __init__(self, img_path_clippy, font, font_size, img_path_w98, img_path_bosd98):
      super().__init__()
      self.qimg = QImage(img_path_w98)
      self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
      self.timer = QTimer(self)
      self.timer.setInterval(3000)
      self.timer.timeout.connect(self.close)
      self.timer.start()
  def closeEvent(self, event):
      super().closeEvent(event)
      cmd = "i3lock -t -i '" + img_path_bosd98 + "'"
      subprocess.run(cmd, shell=True)
    
  def paintEvent(self, qpaint_event):
      # event handler of QWidget triggered when, for ex, painting on the widget’s background.
      painter = QPainter(self)
      rect = qpaint_event.rect() # Returns the rectangle that needs to be updated
      painter.drawImage(rect, self.qimg)
      counter = 0
      
  # def closeAndLock(self):
      # self.close()
      # cmd = 'i3lock -t -i /home/antonio/.config/i3/resources/bosd98.png'
      # subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
      
      

class Main(QWidget):
  def __init__(self, img_path_clippy, font, font_size, distribution, img_path_w98, img_path_eyes, img_path_bosd98):
    super().__init__()
    
    img_clippy = Image.open(img_path_clippy)
    self.width_clippy = img_clippy.width
    self.height_clippy = img_clippy.height
    self.initUI()
  def initUI(self):
    """
    Setting the fonts and the window size, title and properties
    """
    self.window().setFont(QFont(font, font_size))
    self.setGeometry(0,0,self.width_clippy,self.height_clippy)
    QApplication.instance().setFont(QFont(font, font_size))
    self.setWindowTitle('PyQtwidget')
    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    """
    Create a QLabel widget to display the background image
    """
    self.labelBg = QLabel()
    self.labelBg.setPixmap(QPixmap(img_path_clippy))
    """
    Create a QLabel widget to display the the eyes
    """
    self.labelEyes = QLabel()
    self.labelEyes.setPixmap(QPixmap(img_path_eyes))
    self.labelEyes.hide()
    """
    Top label
    """
    self.topLbl = QLabel(self)  
    self.topLbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
    self.topLbl.setContentsMargins(2,2,2,2)
    self.topLbl.setText("It looks like you're are using {}.\nDo you need help to install Windows 98?".format(distribution))
    self.topLbl.setWordWrap(True)
    """
    Label to display while "installing"
    """
    self.installLbl = QLabel(self)  
    self.installLbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
    self.installLbl.setContentsMargins(2,2,2,2)
    self.installLbl.setText("I'm correcting your life mistakes and installing Windows 98...")
    self.installLbl.setWordWrap(True)
    self.installLbl.hide()
    """
    Radio buttons, the fake one that desapeears and cannot be selected and the real one
    """
    self.fakeRadioButton = QRadioButton("Rust off tool!")
    self.fakeRadioButton.setWindowFlags(Qt.WindowType.Window)
    self.fakeRadioButton.setCheckable(False)
    self.realRadioButton = QRadioButton("Yes Master!")
    self.realRadioButton.setWindowFlags(Qt.WindowType.Window)
    self.realRadioButton.clicked.connect(self.goodChoice)
    """
    The check box, unselectable but that shows clippy's red eyes on click
    """
    self.check = QCheckBox("Do not show me \nthis tip again")
    self.check.setContentsMargins(2,2,2,2)
    self.check.installEventFilter(self)
    self.check.setCheckable(False)
    """
    The progress bar of the "installation"
    """
    self.progBar = QProgressBar()
    self.progBar.setGeometry(0, 0, 100, 26)
    self.progBar.setValue(0)
    self.progBar.hide()
    self.progBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.progBar.setStyleSheet(
                      """
                        QProgressBar::chunk {
                          background-color: #010EAC;
                          text-align:center;
                        }
                        QProgressBar::chunk:horizontal {
                          color: white;
                        }
                      """
                          )
    """
    The following is an hack to solve the flickering of the radio button,
    due to the fact that when the button is hidden, an event Leave if the mouse is still on its box
    """
    self.tokenLbl = QLabel(self)
    self.tokenLbl.installEventFilter(self)
    """
    Setting the grid layout
    """
    self.grid = QGridLayout()
    self.grid.setRowMinimumHeight(0, 26)
    self.grid.setRowMinimumHeight(1, 26)
    self.grid.addWidget(self.topLbl, 0, 0)
    self.grid.addWidget(self.installLbl, 1, 0)
    self.grid.addWidget(self.fakeRadioButton, 1, 0)
    self.grid.addWidget(self.tokenLbl, 1, 0)
    self.grid.addWidget(self.realRadioButton, 2, 0)
    self.grid.addWidget(self.progBar, 2, 0)
    self.grid.addWidget(self.check, 3, 0)
    self.grid.setRowStretch(4, 1)
    """
    Setting the stack, this part was mostly generated by chat gpt
    """
    radioWidget = QWidget()
    # Set the radio buttons' layout as the radio widget's layout
    radioWidget.setLayout(self.grid)
    # Add the label widget and the radio widget to the central layout of the window
    self.stackedLayout = QStackedLayout()
    self.stackedLayout.setStackingMode(QStackedLayout.StackingMode.StackAll)
    self.stackedLayout.addWidget(self.labelBg)
    self.stackedLayout.addWidget(self.labelEyes)
    self.stackedLayout.addWidget(radioWidget)
    self.centralLayout = QHBoxLayout()
    self.centralLayout.addLayout(self.stackedLayout)
    self.setLayout(self.centralLayout)
    self.show()
  def goodChoice(self):
    self.topLbl.hide()
    self.fakeRadioButton.hide()
    self.realRadioButton.hide()
    self.check.hide()
    self.tokenLbl.hide()
    self.installLbl.show()
    self.progBar.show()
    """
    Still copied from https://www.pythonguis.com/faq/updating-progressbar-from-qrunner/
    """
    # Thread runner
    self.threadpool = QThreadPool()
    # Create a runner
    self.runner = JobRunner()
    self.runner.signals.progress.connect(self.updateProgress)
    self.threadpool.start(self.runner)
  def updateProgress(self, n):
    self.progBar.setValue(n)
    if n == 100:
      self.close()       
      self.bgWin = FullScreen(img_path_clippy, font, font_size, img_path_w98, img_path_bosd98)
      self.bgWin.showFullScreen()
  def eventFilter(self, source, event):
    """
    Function to hide the fake radio button
    """
    if event.type() == QEvent.Type.Enter and source is self.tokenLbl:
      self.fakeRadioButton.hide()
    elif event.type() == QEvent.Type.Leave and source is self.tokenLbl:
      self.fakeRadioButton.show()
    if event.type() == QEvent.Type.MouseButtonPress and source is self.check:
      self.labelEyes.show()
    elif event.type() == QEvent.Type.Leave and source is self.check:
      self.labelEyes.hide()
    return False

if __name__ == "__main__":
  picFolder = '/home/antonio/.config/i3/resources/pics/'
  img_path_clippy = picFolder + 'clippy1.png'
  img_path_w98 = picFolder + 'w98.png'
  img_path_eyes = picFolder + 'eyes.png'
  img_path_bosd98 = picFolder + 'bosd98.png'
  
  font = 'Windows' # https://www.dafont.com/leviwindows.font
  font_size = 11
  distribution = distro.name()
  #width = img.width
  #height = img.height
  app = QApplication(sys.argv)
  win = Main(img_path_clippy, font, font_size, distribution, img_path_w98, img_path_eyes, img_path_bosd98)
  #win.show()
  sys.exit(app.exec())
