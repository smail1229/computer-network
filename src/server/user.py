from config import *
import json
lock = 0

# set a lock to prevent multithread programming problems
def inlock():
    lock = 1

def unlock():
    lock = 0

class user(object):
    """docstring for user"""
    # users[] is a static class variable which indicates
    # the users finding pairs
    users = []
    def __init__(self):
        super(user, self).__init__()
        self.uid = -1
        self.username = ""
        self.ip = ""
        self.fellow = -1
        #self.storage = data()

    def set(self, userData):
        self.uid = userData["uid"]
        self.username = userData["username"]
        self.ip = userData["ip"]
        self.fellow = userData["fellow"]

    def login(self, username, ip):
        while lock:
            pass
        inlock()
        self.uid = len(self.users) + 1
        newUser = { "uid" : self.uid,
                    "username": username,
                    "ip" : ip,
                    "fellow" : -1,
                  }
        self.users.append(newUser)
        unlock()
        return newUser

    def logout(self):
        while lock:
            pass
        inlock()
        for each in self.users[:]:
            if each["uid"] == self.uid:
                self.users.remove(each)
        unlock()

    def findFellow(self):
        while lock:
            pass
        inlock()
        for each in self.users:
            if each["uid"] != self.uid and each["fellow"] == -1:
                unlock()
                return json.dumps(each)
        unlock()

        return None
