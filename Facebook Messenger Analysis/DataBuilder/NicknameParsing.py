import re
from DataBuilder.MessageInformation import Nickname


def nickname_messages(message_list):
    regex = re.compile('.* set the nickname for .* to .*')
    regex_own = re.compile('.* set (?:her|his|their) own nickname to .*')
    dataowner_regex = re.compile('.* set your nickname to .*')

    nickmsgs = []

    for m in message_list:
        match_other = regex.match(m.Content.__str__())
        match_own = regex_own.match(m.Content.__str__())
        match_dataowner = dataowner_regex.match(m.Content.__str__())
        if match_other or match_own or match_dataowner:
            nickmsgs.append(m)

    return nickmsgs


def nickname_message_parse(message):

    message_text = message.Content

    other_person_regex = re.compile('.* set the nickname for .* to .*')
    own_regex = re.compile('.* set (?:her|his) own nickname to .*')
    dataowner_regex = re.compile('.* set your nickname to .*')

    target_regex = re.compile('((?<= set the nickname for )(.*?)(?= to .*))')
    target_nick_regex = re.compile('((?<= to )(.*)(?=.*)(?=.))')

    own_nick_regex = re.compile('((?<= own nickname to )(.*)(?=.*)(?=.))')

    other_match = other_person_regex.match(message_text)
    own_match = own_regex.match(message_text)
    data_owner_match = dataowner_regex.match(message_text)

    setter = ""
    target = ""
    nickname = ""

    if other_match:
        setter = message.Sender
        target = target_regex.search(message_text).group()
        nickname = target_nick_regex.search(message_text).group()
    elif own_match:
        setter = message.Sender
        target = message.Sender
        nickname = own_nick_regex.search(message_text).group()
    elif data_owner_match:
        setter = message.Sender
        target = "DataOwner"
        nickname = target_nick_regex.search(message_text).group()

    return Nickname(target, setter, message.timestamp, nickname)


def reconstruct_nicknames(chat_history):

    message_history = chat_history.ChatMessages

    nick_msgs = nickname_messages(message_history)

    participants = chat_history.ChatParticipants

    for m in nick_msgs:
        nick = nickname_message_parse(m)
        target = nick.ParticipantName
        if target == "DataOwner":
            nick.ParticipantName = chat_history.DataOwner

        participants[nick.ParticipantName].Nicknames.append(nick)
