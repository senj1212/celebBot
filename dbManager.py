from models.bdCreator import Session, db_create, engine, metadata, Base
from models.users import Users
from models.profiles import Profiles
from models.messages import Messages
from models.unreads import Unreads
from models.onlines import Onlines
import random


class DataBaseManager():
    def __init__(self):
        db_create()

        self.status_users={
            "processed": 0,
            "black_list": 1
        }
        self.status_msg = {
            "send": 1,
            "not_send": 0
        }


    def getAllTable(self):
        return engine.table_names()

    def getColumsNamesFromTable(self, table_name):
        return metadata.tables[table_name].columns.keys()

    def getAllDataFromTable(self, tables_name):
        for mapper in Base.registry.mappers:
            cls = mapper.class_
            if str(cls.__table__) == str(tables_name):
                session = Session()
                data = session.query(cls).all()
                result = [i.get_list() for i in data]
                session.close()
                return result
        return None

    def getChangedTable(self, tables_name):
        if tables_name == 'messages' or tables_name == 'profiles':
            return True
        return False


    def addOnlineUsers(self, user_id, user_lvl, user_name):
        session = Session()
        all_users = session.query(Users).filter(Users.user_id == user_id)
        online_user = session.query(Onlines).filter(Onlines.user_id == user_id)
        unread_user = session.query(Unreads).filter(Unreads.user_id == user_id)
        if bool(online_user.count()) or bool(all_users.count()) or bool(unread_user.count()):
            session.close()
            return False
        session.add(Onlines(user_id = user_id, user_lvl = user_lvl, user_name = user_name))
        session.commit()
        session.close()
        print(f"add {user_name}")
        return True

    def getOnlineUsers(self, profile_id=0, all=False):
        result = None
        session = Session()
        online_users = session.query(Onlines).all()
        if all:
            return online_users
        for user in online_users:
            worked = str(user.profile_worked).split(',')
            if str(profile_id) not in worked:
                result = {
                    'user_id': user.user_id,
                    'user_lvl': user.user_lvl,
                    'user_name': user.user_name
                }
        session.close()
        return result

    def processingOnlineUsers(self, user_id, profile_id):
        session = Session()
        online_users = session.query(Onlines).filter(Onlines.user_id == user_id)
        if bool(online_users.count()):
            online_user = online_users[0]
            online_user.count_worked = int(online_user.count_worked) + 1
            count = int(online_user.count_worked)
            online_user.profile_worked += f",{profile_id}"
            try:
                session.commit()
                if count >= len(session.query(Profiles).all()):
                    self.removeOnlineUser(user_id)

            except:
                print(f"Error 69 {user_id} {profile_id}")
        session.close()


    def removeOnlineUser(self, user_id):
        session = Session()
        online_user = session.query(Onlines).filter(Onlines.user_id == user_id)
        if bool(online_user.count()):
            session.delete(online_user[0])
            session.commit()
            self.addUser(user_id, self.status_users["processed"])
        session.close()

    def addUser(self, user_id, status):
        session = Session()
        session.add(Users(user_id = user_id, status = status))
        session.commit()
        session.close()

    def getUsers(self):
        session = Session()
        result = session.query(Users).all()
        session.close()
        return result

    def addProfile(self, login, password):
        session = Session()
        profiles = session.query(Profiles).filter(Profiles.login == login)
        if bool(profiles.count()):
            session.close()
            return False
        session.add(Profiles(login=login, password=password))
        session.commit()
        session.close()

    def updateProfile(self, id, login, password, status):
        session = Session()
        profile = session.query(Profiles).filter(Profiles.id == id)
        if bool(profile.count()):
            profile[0].login = login
            profile[0].password = password
            profile[0].status = status
        session.commit()
        session.close()

    def getProfile(self, login=None):
        result = []
        session = Session()
        if login is None:
            for i in session.query(Profiles).all():
                result.append({
                    "id": i.id,
                    "login": i.login,
                    "password": i.password,
                    "status": i.status
                })
            session.close()
            return result
        profiles = session.query(Profiles).filter(Profiles.login == login)
        if bool(profiles.count()):
            result = {
                "id": profiles[0].id,
                "login": login,
                "password": profiles[0].password,
                "status": profiles[0].status
            }
        session.close()
        return result

    def removeProfile(self, login=None, id=None):
        session = Session()
        if login is not None:
            profile = session.query(Profiles).filter(Profiles.login == login)[0]
        if id is not None:
            profile = session.query(Profiles).filter(Profiles.id == id)[0]
        session.delete(profile)
        session.commit()
        session.close()

    def addMessage(self, msg, profile_id, status):
        session = Session()
        session.add(Messages(status=status, msg=msg, profile_id=profile_id))
        session.commit()
        session.close()

    def updateMessage(self, id, text, profile_id, status):
        session = Session()
        msg = session.query(Messages).filter(Messages.id == id)
        if bool(msg.count()):
            msg[0].msg = text
            msg[0].status = status
            msg[0].profile_id = profile_id
        session.commit()
        session.close()

    def getMessage(self, profile_id):
        msg = None
        session = Session()
        messages = session.query(Messages).filter(Messages.profile_id == profile_id).filter(Messages.status == self.status_msg['send'])
        if messages.count() > 0:
            msg = messages[random.randint(0, messages.count() - 1)].msg
        session.close()
        return msg

    def removeMessage(self, msg_id):
        session = Session()
        messages = session.query(Messages).filter(Messages.id == msg_id)
        if messages.count() > 0:
            session.delete(messages[0])
        session.commit()
        session.close()

    def addUnread(self, user_id, profile_id, url):
        session = Session()
        unreads = session.query(Unreads).filter(Unreads.profile_id == profile_id).filter(
            Unreads.user_id == user_id)
        if unreads.count() < 1:
            session.add(Unreads(user_id = user_id, url = url, profile_id = profile_id))
            session.commit()
        session.close()

    def getUnreads(self):
        unreads = []
        session = Session()
        unread = session.query(Unreads).all()
        for i in unread:
            unreads.append({
                'id': i.id,
                'user_id': i.user_id,
                'url': i.url,
                'profile_id': i.profile_id
            })
        session.close()
        return unreads

    def removeUnread(self, id):
        session = Session()
        unreads = session.query(Unreads).filter(Unreads.id == id)
        if unreads.count() > 0:
            session.delete(unreads[0])
        session.commit()
        session.close()