import datetime
import re

from DataBuilder.ChatParsing import ChatHistory
from DataBuilder.MessageParsing import Message
from DataBuilder.ParticipantParsing import Participant


class MembershipRecord(object):

    def __init__(self, message: Message,
                 timestamp: datetime.datetime,
                 record_type: str, actor: Participant or None,
                 target: Participant, estimate: bool = False) -> None:
        self.OriginalMessage = message
        self.timestamp = timestamp
        self.RecordType = record_type
        self.Actor = actor
        self.Target = target
        self.Estimate = estimate

    def __str__(self):
        str = "\nActor: " + self.Actor.Name + \
              "\nDate: " + self.timestamp.__str__() + \
              "\nRecord Type: " + self.RecordType + \
              "\nEstimate: " + self.Estimate.__str__()
        return str


def membership_history_reconstruction(chat_history: ChatHistory) -> None:
    for m in chat_history.ChatMessages:
        potential,type = _isPotentialHistory(m)

        if potential:
            record = _parse_historical_message()

            if record is not None:



def _isPotentialHistory(message_text: str) -> (bool, str):
    message_text = message_text.lower()

    if "added" in message_text:
        return True, "ADD"

    if "left" in message_text:
        return True, "LEFT"

    if "removed" in message_text:
        return True, "REMOVED"

    return False, ""


def _parse_historical_message(message_text: str,) -> (bool, str):
    pass
