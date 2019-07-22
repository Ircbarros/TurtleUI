# -*- coding: utf-8 -*-
# !/usr/bin/env python2
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
# import Wnck, Gdk


class Container(QtWidgets.QTabWidget):
    def __init__(self):
        QtWidgets.QTabWidget.__init__(self)
        self.embed('RViz')

    def embed(self, command, *args):
        proc = QtCore.QProcess()
        proc.setProgram(command)
        proc.setArguments(args)
        started, procId = proc.startDetached()
        if not started:
            QtWidgets.QMessageBox.critical(self, 'Command "{}" not started!')
            return
        attempts = 0
        while attempts < 10:
            screen = Wnck.Screen.get_default()
            screen.force_update()
            # this is required to ensure that newly mapped window get listed.
            while Gdk.events_pending():
                Gdk.event_get()
            for w in screen.get_windows():
                if w.get_pid() == procId:
                    window = QtGui.QWindow.fromWinId(w.get_xid())
                    container = QtWidgets.QWidget.createWindowContainer(window, self)                    
                    self.addTab(container, command)
                    return
            attempts += 1
        QtWidgets.QMessageBox.critical(self, 'Window not found', 'Process started but window not found')


app = QtWidgets.QApplication(sys.argv)
w = Container()
w.show()
sys.exit(app.exec_())