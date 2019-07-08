import datetime
import re

from DataProcess.models.messageTypes import regexExpressions
from DataProcess.models.Person import Nickname

class Message(object):

    def __init__(self, orig_json, chat_history):
        self.OriginalJson = orig_json
        self.sender_name = orig_json["sender_name"]
        self.timestamp = datetime.datetime.fromtimestamp(orig_json['timestamp_ms']/1000)

    @staticmethod
    def message_creator(json, chat_history):
        if json["type"] == "Generic" and "content" in json:

            if re.fullmatch(regexExpressions["OtherNicknameSet"], json["content"]):
                return OtherNicknameSet(json, chat_history)

            if re.fullmatch(regexExpressions["SelfNicknameSet"], json["content"]):
                return SelfNicknameSet(json, chat_history)

        if json["type"] == "Subscribe":
            return AddMember(json, chat_history)
        if json["type"] == "Unsubscribe":
            if json["users"][0]["name"] == json["sender_name"]:
                return LeaveMember(json, chat_history)
            return RemoveMember(json, chat_history)


        return Generic(json, chat_history)


class AddMember(Message):
    pass


class RemoveMember(Message):
    pass


class LeaveMember(Message):
    pass


class Generic(Message):
    pass


class OtherNicknameSet(Message):
    def __init__(self, orig_json, chat_history):
        super().__init__(orig_json, chat_history)

        nick = Nickname(orig_json, chat_history)
        chat_history.NicknameLookup[nick.nickname] = nick


class SelfNicknameSet(Message):
    pass


class ThisSelfNicknameSet(Message):
    pass


class ThisOtherNicknameSet(Message):
    pass


class CreatePoll(Message):
    pass


class PollVote(Message):
    pass
