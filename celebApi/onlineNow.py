from time import sleep

class GetOnlineNow:
    def __init__(self, session):
        self.session = session
        self.urlOnline = "https://api.celeb.tv/api/v2/online-now"
        self.urlUser = "https://api.celeb.tv/api/v1/profile/"
        self.black_list = []
        self.work = False


    def get(self, dbManager, minLevel = 2, timeout= 0, ):
        print("start")
        self.work = True
        while self.work:
            response = self.session.get(self.urlOnline)
            for user in response.json():
                lvl = self.checkUserLvl(user["username"])
                if lvl >= minLevel and user["username"] not in self.black_list:
                    dbManager.addOnlineUsers(user["user_id"], lvl, user["username"])
                sleep(timeout)
            if len(dbManager.getOnlineUsers(all=True)) > 20:
                self.work = False

    def checkUserLvl(self, nick):
        response = self.session.get(self.urlUser + nick)
        return int(response.json()["level_info"]["level"])

    def updateBlackList(self):
        with open("black.txt", "r") as blackList:
            self.black_list = blackList.read().split("\n")
