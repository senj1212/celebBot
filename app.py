from profile import Profile
import dbManager
import threading
from settings import GUI
from time import sleep

db = dbManager.DataBaseManager()

RUN = True

def main(login):
    global RUN
    prof = None
    if prof is None:
        prof = Profile(login, db)
        while not prof.authManager.authCheck:
            if not RUN:
                break
        prof.initializeTools()
    while RUN:
        res = prof.nextSendMsg()

    print(f"stoped {login}")
    prof.driver.close()


def menu():
    global RUN
    while True:
        command = input(">>> ")
        if command == "stop":
            RUN = False
            break
        elif command == 'gui':
            gui = GUI(db)
            gui.run()
        elif command == 'start':
            for i in db.getProfile():
                threadmain = threading.Thread(target=main, args=(i["login"],))
                threadmain.start()

if __name__ == "__main__":
    menu()