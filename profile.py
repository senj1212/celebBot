import celebApi
import threading
from time import sleep

NAME_ROJECT = "OnlyFans bot"
VERSION = '1.0'

class Profile:
    def __init__(self, login, dbManager):
        self.dbManager = dbManager
        self.profile_info = self.dbManager.getProfile(login)
        self.authManager = celebApi.Authorization(self.profile_info['login'], self.profile_info['password'])
        self.session = None
        self.driver = None
        self.driverWite = None
        self.authManager.auth()
        self.new_meesage = False

    def setData(self):
        resultAuth = self.authManager.get()
        self.session = resultAuth['session']
        self.driver = resultAuth['driver']
        self.driverWite = resultAuth['wite']

    def initializeTools(self):
        self.setData()
        self.onlineManager = celebApi.GetOnlineNow(self.session)
        self.unreadManager = celebApi.CheckUnread(self.session)
        self.msgManager = celebApi.MessageManager(self.session, self.driver, self.driverWite, self.dbManager)
        self.driver.minimize_window()

    def startCheckerOnlineUsers(self, minLevel, timeout):
        if not self.onlineManager.work:
            self.threadCheck = threading.Thread(target=self.onlineManager.get, daemon=True, args=(self.dbManager, minLevel, timeout, ))
            self.threadCheck.start()
        else:
            print("not start")

    def startCheckerUnread(self):
        def threadChecker():
            if self.unreadManager.check():
                self.new_meesage = True

        if not self.unreadManager.work:
            self.threadCheckUnread = threading.Thread(target=threadChecker, daemon=True)
            self.threadCheckUnread.start()

    def nextSendMsg(self):
        user = self.dbManager.getOnlineUsers(profile_id = self.profile_info["id"])
        if user is None:
            sleep(2)
            self.startCheckerOnlineUsers(2, 0.2)
            return "Not users online"
        text_msg = self.dbManager.getMessage(self.profile_info["id"])
        if text_msg is None:
            return "Not text msg in profile"
        res = self.msgManager.sendMsg(text_msg, user['user_id'])
        self.dbManager.processingOnlineUsers(user['user_id'], self.profile_info["id"])
        return {"from": self.profile_info["login"],
                "to": user['user_id'],
                "text": text_msg,
                "status": res}
