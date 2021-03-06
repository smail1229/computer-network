#coding:utf-8

from PyQt4 import QtCore, QtGui, QtWebKit

import chat
import login
import threading
import os
import user
import sys
import socket
reload(sys)
sys.setdefaultencoding('utf8')

username_local = ""
username_remote = ""
server_name_remote = ""
server_name_local  = socket.gethostbyname(socket.gethostname())

@QtCore.pyqtSlot()
def setRemote(user_remote):
    global username_remote
    username_remote = user_remote.username
    global server_name_remote
    server_name_remote = user_remote.ip

class Floater(QtCore.QObject):
    @QtCore.pyqtSlot(str)
    def showMessage(self, msg):
        """Open a message box and display the specified message."""
        QtGui.QMessageBox.information(None, "hahhahah", msg)

    @QtCore.pyqtSlot()
    def getUsername(self):
        return username_local

    @QtCore.pyqtSlot()
    def getRemotename(self):
        return username_remote

    @QtCore.pyqtSlot(str)
    def setUsername(self, message):
        global username_local
        username_local = message

    @QtCore.pyqtSlot()
    def searchThread(self):
        t3 = threading.Thread(target=login.getUser, args=(username_local,server_name_local))
        t3.start()

    @QtCore.pyqtSlot()
    def aaa(self):
        return username_remote

    @QtCore.pyqtSlot()
    def getRemote(self):
        if username_remote == "":
            return True;
        else:
            return False;

    @QtCore.pyqtSlot()
    def setThreads(self):
        print username_remote, server_name_local
        print username_local, server_name_remote
        t1 = threading.Thread(target=chat.receive, args=(username_remote, server_name_local))
        # thread t2 is a socket that listen a port in local and send message to remote
        t2 = threading.Thread(target=chat.send, args=(username_local, server_name_remote))
        t1.start()
        t2.start()


    @QtCore.pyqtSlot(str)
    def send(self, message):
        chat.send_queue.put("%s" % (message))

    @QtCore.pyqtSlot()
    def receive(self):
        if chat.receive_queue.empty():
            return ""
        message = chat.receive_queue.get()
        chat.receive_queue.task_done()
        message = message.decode('utf-8')
        return message

    receiveMsg = QtCore.pyqtProperty(str, fget=receive)
    username = QtCore.pyqtProperty(str, fget=getUsername)
    remotename = QtCore.pyqtProperty(str, fget=getRemotename)
    isLogin = QtCore.pyqtProperty(bool, fget=getRemote)
