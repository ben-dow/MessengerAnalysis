import re
from DataProcess.models.messageTypes import regexExpressions

your = "Benjamin Dow"


class Person:

    def __init__(self, display_name):
        self.DisplayName = display_name

        self.Messages = []

        self.Nicknames = []

        self.JoinDates = []
        self.LeaveDates = []


class Nickname:

    def __init__(self, msg_json, chat_history):
        regex_match = re.fullmatch(regexExpressions["OtherNicknameSet"], msg_json["content"])
        setter = msg_json["sender_name"]

        reg_name = regex_match.group(2)
        if regex_match.group(3) is not None:
            reg_name = your

        self.setter = chat_history.get_person(setter)
        self.target = chat_history.get_person(reg_name)
        self.nickname = regex_match.group(4)

        self.target.Nicknames.append(self)

        def __str__(self):
            return self.nickname

        def __repr__(self):
            return self.__str__()
