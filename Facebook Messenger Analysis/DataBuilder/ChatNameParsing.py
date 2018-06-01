import re

from DataBuilder.MessageInformation import Message, ChatHistory


class ChatNameRecord(object):

    def __init__(self, message:Message, chatName: str) -> None:
        self.OriginalMessage = message
        self.Timestamp = message.timestamp
        self.Actor = message.Sender
        self.ChatName = chatName

    def __str__(self) -> str:
        """
        Creates a string representation of a nickname object
        :return: The string representation
        """
        return_str = self.Actor + " set the groups name to " + \
                     self.ChatName + " on " + \
                     self.Timestamp.__str__()
        return return_str


def chat_renamed_reconstruction(chat_history: ChatHistory):

    chat_messages = chat_history.ChatMessages

    for m in chat_messages:
        if _check_message_of_type(m):
            _process_chat_message(m,chat_history)


def _check_message_of_type(message):
    regex = re.compile('.* named the group .*')
    regex_match = regex.search(message.Content.__str__())
    if regex_match:
        return True

    return False


def _process_chat_message(message, chat_history):

    nick = _nickname_of_actor(message)
    name = _name_of_chat(message)

    # Check that nickname is in the actors list of nicknames
    partic = chat_history.ChatParticipants[message.Sender]
    if nick in partic.Nicknames.keys() or nick == ("You" or " You"):
        new_name = ChatNameRecord(message,name)
        chat_history.ChatNameHistory.append(new_name)


def _nickname_of_actor(message):
    regex = re.compile('.*(?= named the group.*(?:.|!|\?|))')
    regex_match = regex.search(message.Content.__str__())
    return regex_match.group()

def _name_of_chat(message):
    regex = re.compile('(?<= named the group ).*(?=.|!|\?|)')
    regex_match = regex.search(message.Content.__str__())

    return regex_match.group()