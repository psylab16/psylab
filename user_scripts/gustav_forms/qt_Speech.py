# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import time
from datetime import datetime

class Interface():
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.dialog = self.Dialog()

    class Dialog(QtGui.QDialog):

        def __init__(self, parent=None):
            QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowTitleHint)
            #self.setWindowIcon(QtGui.QIcon('icon.png'))
            self.setFixedWidth(400)
            self.char = ''
            self.waitingForResponse = False
            self.quitKey = '/'

            self.ctimer = QtCore.QTimer()
            QtCore.QObject.connect(self.ctimer, QtCore.SIGNAL("timeout()"), self.updateClock)
            self.ctimer.start(1000)
            vbox = QtGui.QVBoxLayout()
            #vbox.addStretch(1)

            headerBox = QtGui.QHBoxLayout()

            self.isPlaying = QtGui.QLabel('PlayBack!')
            self.isPlaying.setStyleSheet("QWidget { background-color: 'red'; border: 1px solid darkRed; margin-left: 10; margin-right: 10; margin-top: 8; margin-bottom: 8 }")
            f = self.isPlaying.font()
            f.setPointSize(14)
            self.isPlaying.setFont(f)
            headerBox.addWidget(self.isPlaying)
            headerBox.addStretch(1)

            #self.isPlaying.setVisible(False)

            self.timeLabel = QtGui.QLabel()
            self.timeLabel.setStyleSheet("QWidget { border: 1px solid black; margin-left: 10; margin-right: 10; margin-top: 8; margin-bottom: 8 }")
            f = self.timeLabel.font()
            f.setPointSize(14)
            self.timeLabel.setFont(f)
            headerBox.addWidget(self.timeLabel)
            vbox.addLayout(headerBox)

            self.expLabel = QtGui.QLabel()
            f = self.expLabel.font()
            f.setPointSize(10)
            self.expLabel.setFont(f)
            self.expLabel.setStyleSheet("QWidget { border: 1px solid darkGray; }")
            vbox.addWidget(self.expLabel)

            self.blockLabel = QtGui.QLabel()
            f = self.blockLabel.font()
            f.setPointSize(10);
            self.blockLabel.setFont(f)
            self.blockLabel.setStyleSheet("QWidget { border: 1px solid darkGray; vertical-align: text-top; }")
            self.blockLabel.setAlignment(QtCore.Qt.AlignTop)
            vbox.addWidget(self.blockLabel)

            self.trialLabel = QtGui.QLabel()
            f = self.trialLabel.font()
            f.setPointSize(10);
            self.trialLabel.setFont(f)
            self.trialLabel.setFixedHeight(60)
            self.trialLabel.setStyleSheet("QWidget { border: 1px solid darkGray; }")
            self.trialLabel.setAlignment(QtCore.Qt.AlignTop)
            self.trialLabel.setWordWrap(True)
            vbox.addWidget(self.trialLabel)

            scoreBox = QtGui.QHBoxLayout()

            self.trialScore = QtGui.QLabel()
            f = self.trialScore.font()
            f.setPointSize(10);
            self.trialScore.setFont(f)
            self.trialScore.setFixedHeight(60)
            self.trialScore.setStyleSheet("QWidget { border: 1px solid darkGray; }")
            self.trialScore.setAlignment(QtCore.Qt.AlignTop)
            scoreBox.addWidget(self.trialScore)

            self.blockScore = QtGui.QLabel()
            f = self.blockScore.font()
            f.setPointSize(10);
            self.blockScore.setFont(f)
            self.blockScore.setFixedHeight(60)
            self.blockScore.setStyleSheet("QWidget { border: 1px solid darkGray; }")
            self.blockScore.setAlignment(QtCore.Qt.AlignTop)
            scoreBox.addWidget(self.blockScore)

            vbox.addLayout(scoreBox)

            ConditionBox = QtGui.QHBoxLayout()

            self.blockVariables = QtGui.QLabel()
            f = self.blockVariables.font()
            f.setPointSize(10);
            self.blockVariables.setFont(f)
            self.blockVariables.setFixedHeight(120)
            self.blockVariables.setStyleSheet("QWidget { border: 1px solid darkGray; }")
            self.blockVariables.setAlignment(QtCore.Qt.AlignTop)
            ConditionBox.addWidget(self.blockVariables)

            self.expVariables = QtGui.QLabel()
            f = self.expVariables.font()
            f.setPointSize(10);
            self.expVariables.setFont(f)
            self.expVariables.setFixedHeight(120)
            self.expVariables.setStyleSheet("QWidget { border: 1px solid darkGray; }")
            self.expVariables.setAlignment(QtCore.Qt.AlignTop)
            ConditionBox.addWidget(self.expVariables)

            vbox.addLayout(ConditionBox)

            cbox = QtGui.QHBoxLayout()

            self.blocks = QtGui.QLabel("")
            cbox.addWidget(self.blocks)

            cbox.addStretch(1)

            cancelButton = QtGui.QPushButton("Cancel")
            cancelButton.clicked.connect(self.closeEvent)
            cbox.addWidget(cancelButton)

            vbox.addLayout(cbox)
            self.setLayout(vbox)

            self.setWindowTitle("Gustav!")
            self.setModal=False
            self.show()
            self.setFixedSize(self.width(),self.height()) # <- Must be done after show


        def updateClock(self):
            now = datetime.now()
            self.timeLabel.setText('%02i:%02i:%02i' % (now.hour,now.minute,now.second))

        def closeEvent(self, event):
            # fake a quit:
            self.waitingForResponse = True
            self.keyDown(ord(self.quitKey))

        def keyPressEvent(self, event):
            self.keyDown(event.key())

        def keyReleaseEvent(self, event):
            self.keyUp(event.key())

        def keyDown(self, key):
            if self.waitingForResponse:
                if key < 256:
                    thiskey = chr(key).lower()
                    self.char = thiskey
                    self.waitingForResponse = False

        def keyUp(self, key):
            if key == QtCore.Qt.Key_Control:
                ctrlDown = False
            elif key == QtCore.Qt.Key_Shift:
                shiftDown = False
            elif key == QtCore.Qt.Key_Alt:
                altDown = False

    # End Dialog

    def get_resp(self):
        """Waits modally for a keypress
        """
        self.dialog.waitingForResponse = True
        sys.stdout.flush() # In case the output of a prior print statement has been buffered
        while self.dialog.waitingForResponse:
            self.app.processEvents()
            time.sleep(.1)
        curchar = self.dialog.char
        self.dialog.char = ''
        return curchar

    def showPlaying(self, playing):
        self.dialog.isPlaying.setVisible(playing)
        self.update_form()

    def updateInfo_Exp(self, s):
        self.dialog.expLabel.setText(s)
        self.update_form()

    def updateInfo_Block(self, s):
        self.dialog.blockLabel.setText(s)
        self.update_form()

    def updateInfo_Trial(self, s):
        self.dialog.trialLabel.setText(s)
        self.update_form()

    def updateInfo_BlockScore(self, s):
        self.dialog.blockScore.setText(s)
        self.update_form()

    def updateInfo_TrialScore(self, s):
        self.dialog.trialScore.setText(s)
        self.update_form()

    def updateInfo_blockVariables(self, s):
        self.dialog.blockVariables.setText(s)
        self.update_form()

    def updateInfo_expVariables(self, s):
        self.dialog.expVariables.setText(s)
        self.update_form()

    def updateInfo_BlockCount(self, s):
        self.dialog.blocks.setText(s)
        self.update_form()
        
    def update_form(self):
        # have to call this twice or some widgets won't update
        self.app.processEvents()
        self.app.processEvents()
