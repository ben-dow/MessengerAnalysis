import re
from DataBuilder.MessageInformation import Nickname, Message, ChatHistory


def nickname_messages(message_list: list) -> list:
    """
    Find all of the messages within the list of messages given that are a changing of a nickname

    :param message_list: A list of messages
    :return: The list of nickname messages
    """
    other_person_regex = \
        re.compile('.* set the nickname for .* to .*')  # Regex to find nicknames changed by another person

    own_regex = \
        re.compile('.* set (?:her|his|their) own nickname to .*')  # Regex to find nicknames changed by the same person

    data_owner_regex = \
        re.compile('.* set your nickname to .*')  # Regex to find nickname changing of the data owner

    nickmsgs = []  # Initiate the list of Nickname Messages

    for m in message_list:

        # Try to Match Each of the regex described above
        match_other = other_person_regex.match(m.Content.__str__())
        match_own = own_regex.match(m.Content.__str__())
        match_dataowner = data_owner_regex.match(m.Content.__str__())

        if match_other or match_own or match_dataowner:  # If even one matches it means its a nickname message
            nickmsgs.append(m)  # Add the message to the list of messages

    return nickmsgs


def nickname_message_parse(message: Message) -> Nickname:
    """
    Parse an individual message for nickname information using Regex

    :param message: The message to be parsed
    :return: A nickname object containing information about the nickname
    """
    message_text = message.Content  # Get the content of the message for ease of use

    ''' Regex Setups '''

    '''Regex for General Nickname/Message Type'''
    other_person_regex =\
        re.compile('.* set the nickname for .* to .*')  # Regex for Nickname set by a third party for a different third party

    own_regex =\
        re.compile('.* set (?:her|his) own nickname to .*')  # Regex for a Nickname set by a third party for the same third party

    dataowner_regex =\
        re.compile('.* set your nickname to .*') # Regex for a Nickname set by a third party for the Data Owner

    ''' Regex for Finding Nickname "Wearer" '''
    target_regex =\
        re.compile('((?<= set the nickname for )(.*?)(?= to .*))')  # Regex for the full FB Name of the "wearer" of the nickname

    '''Regex for Finding the Nickname'''
    target_nick_regex =\
        re.compile('((?<= to )(.*)(?=.*)(?=.))')  # Regex for the Nickname

    own_nick_regex = re.compile('((?<= own nickname to )(.*)(?=.*)(?=.))') # Regex for the Nickname from a Third Party to Same Third Party

    '''Execute the Match of the General Nickname/Message Type'''
    other_match = other_person_regex.match(message_text)
    own_match = own_regex.match(message_text)
    data_owner_match = dataowner_regex.match(message_text)

    '''Initiate the Key pieces of data for the nickname'''
    setter = ""
    target = ""
    nickname = ""

    if other_match:   # If third party for a different third party
        setter = message.Sender
        target = target_regex.search(message_text).group()
        nickname = target_nick_regex.search(message_text).group()
    elif own_match:   # If third party for the same third party
        setter = message.Sender
        target = message.Sender
        nickname = own_nick_regex.search(message_text).group()
    elif data_owner_match: # If third party for the Data Owner
        setter = message.Sender
        target = "DataOwner"
        nickname = target_nick_regex.search(message_text).group()

    return Nickname(target, setter, message.timestamp, nickname)


def reconstruct_nicknames(chat_history: ChatHistory) -> None:
    """
    Function to initiate the reconstruction of Nickname History from a chat history
    :param chat_history: The Chat History
    """
    message_history = chat_history.ChatMessages  # Get the Messages for ease of calling

    nick_msgs = nickname_messages(message_history)  # Get the Nickname messages

    participants = chat_history.ChatParticipants  # Get the Participant List for the Chat history

    for m in nick_msgs:  # Handle each Message individually

        nick = nickname_message_parse(m)  # Get the Nickname Object for Manipulation
        target = nick.ParticipantName  # Get the Participant who this applies to (the "target")

        if target == "DataOwner":  # Check to see if DataOwner was the target.
            nick.ParticipantName = chat_history.DataOwner  # If so, update that with the actual name of the data owner

        participants[nick.ParticipantName].Nicknames.\
            append(nick)  # Place the nickname data directly into the object representing the Participant
