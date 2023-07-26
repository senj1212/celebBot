import json

class CheckUnread:
    def __init__(self, session):
        self.session = session
        self.url = "https://api.celeb.tv/api/v1/chatsddb/unreads"
        self.has_unread_url = 'https://api.celeb.tv/api/v1/chatsddb/has_unread_messages'
        self.work = False

    def check(self):
        response = self.session.get(self.has_unread_url)
        print(response.json['has_unread_messages'])
        return False
