import datetime
import re

from DataBuilder.MessageInformation import ChatHistory, Message, Participant


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


def person__added_or_removed__reconstruction(chat_history: ChatHistory) -> None:
    """

    :param chat_history:
    :return:
    """

    message_type_switch = {
        "ADDED": _process_added_message,
        "REMOVED": _process_removed_message,
        "LEFT": _process_left_message,
        "NONE": None
    }

    ''' Chat Mesages for Ease of Calling '''
    chat_messages = chat_history.ChatMessages

    potential_messages = []

    for m in chat_messages:
        member = _check_if_member_message(m, chat_history)

        if member:
            potential_type = _check_potential_type(m)
            potential_messages.append((m, potential_type))

    for m, t in potential_messages:  # Construct the Membership History from Messages Sent to Chat
        message_type_switch[t](m, chat_history)

    _construct_original_membership(chat_history)


def _construct_original_membership(chat_history: ChatHistory):
    people = chat_history.ChatParticipants
    chat_history.ChatMessages.sort(key=lambda x: x.timestamp, reverse=False)
    messages = chat_history.ChatMessages

    for p in people:

        people[p].MemberShipRecords.sort(key=lambda x: x.timestamp, reverse=False)
        persons_records = people[p].MemberShipRecords

        if (len(persons_records) == 0 and len(people[p].Messages) > 0) or \
                persons_records[0].RecordType == ("REMOVED" or "LEFT"):
            people[p].Messages.sort(key=lambda x: x.timestamp)
            first_message = people[p].Messages[0]
            record = MembershipRecord(first_message, first_message.timestamp, "ADDED", None, people[p], True)
            people[p].MemberShipRecords.append(record)
            people[p].Messages.sort(key=lambda x: x.timestamp)
        elif len(persons_records) == 0 and len(people[p].Messages) == 0:
            first_message = messages[0]
            record = MembershipRecord(first_message, first_message.timestamp, "ADDED", None, people[p], True)
            people[p].MemberShipRecords.append(record)


def _check_if_member_message(message: Message, chat_history: ChatHistory) -> bool:
    ''' Compile Regex for Finding the Right Messages'''
    correct_format_regex = \
        re.compile(
            '.* (?:added|removed|left).*.')  # Check if Potential Message is of the acceptable format to be an added message

    correct_format = correct_format_regex.match(message.Content.__str__())

    if correct_format \
            and not _check_if_poll(message.Content.__str__()) \
            and not _check_if_plan(message.Content.__str__()) \
            and _nick_matches_sender(message, chat_history):
        return True

    return False


def _check_if_poll(message: str):
    removed_vote_regex = re.compile('.* removed vote for .* in the poll: .*')

    if removed_vote_regex.match(message):
        return True
    else:
        return False


def _check_if_plan(message: str):
    removed_plan_regex = re.compile('.* removed the plan location.')

    if removed_plan_regex.match(message):
        return True
    else:
        return False


def _check_potential_type(message: Message) -> str:
    if "added" in message.Content.__str__():
        return "ADDED"
    elif "removed" in message.Content.__str__():
        return "REMOVED"
    elif "left" in message.Content.__str__():
        return "LEFT"
    else:
        return "NONE"


def _process_removed_message(message: Message, chat_history: ChatHistory):
    get_name_regex = re.compile('(?<=removed ).*(?= from the group)')

    match = get_name_regex.search(message.Content.__str__()).group()

    chat_history.ChatParticipants[match].MemberShipRecords.append(
        MembershipRecord(message,
                         message.timestamp,
                         "REMOVED",
                         chat_history.ChatParticipants[message.Sender],
                         chat_history.ChatParticipants[match]))


def _process_added_message(message: Message, chat_history):
    names_added_regex = re.compile('(?<=added ).*(?=.)')

    names = names_added_regex.search(message.Content.__str__()).group()

    if " and " in names:
        separate_names_regex = re.compile('(.*)(?= and )|(?<= and )(.*)')
        separate_names = separate_names_regex.findall(names)

        first_person = separate_names[0][0]
        second_person = separate_names[2][1]

        chat_history.ChatParticipants[first_person].MemberShipRecords.append(
            MembershipRecord(message,
                             message.timestamp,
                             "ADDED",
                             chat_history.ChatParticipants[message.Sender],
                             chat_history.ChatParticipants[first_person]))

        check_actual_person_regex = re.compile('[0-9]* others')
        match = check_actual_person_regex.search(second_person)

        if not match:
            chat_history.ChatParticipants[second_person].MemberShipRecords.append(
                MembershipRecord(message,
                                 message.timestamp,
                                 "ADDED",
                                 chat_history.ChatParticipants[message.Sender],
                                 chat_history.ChatParticipants[second_person]))

    else:
        chat_history.ChatParticipants[names].MemberShipRecords.append(
            MembershipRecord(message,
                             message.timestamp,
                             "ADDED",
                             chat_history.ChatParticipants[message.Sender],
                             chat_history.ChatParticipants[names]))


def _process_left_message(message: Message, chat_history):
    chat_history.ChatParticipants[message.Sender].MemberShipRecords.append(
        MembershipRecord(message,
                         message.timestamp,
                         "LEFT",
                         chat_history.ChatParticipants[message.Sender],
                         chat_history.ChatParticipants[message.Sender]))


def _nick_actor(message: str) -> str:
    potential_adder_regex = \
        re.compile("((.*)(?=(?: added| removed| left).*))")  # Get the Nickname of the potential adder
    nick = potential_adder_regex.match(message).group()
    return nick


def _nick_matches_sender(message, chat_history):
    actor_nick = _nick_actor(message.Content.__str__())

    if actor_nick == "You":
        actor_nick = chat_history.DataOwner

    if actor_nick in chat_history.ChatParticipants[message.Sender].Nicknames or actor_nick == message.Sender:
        return True

    return False
