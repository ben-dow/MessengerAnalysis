import datetime
from DataBuilder.MessageInformation import ChatHistory

"""
Functions to return lists of Messages based on criteria
Created by Benji Dow on 5/19/2018
"""


def all_messages(chat_history: ChatHistory) -> list:
    """
    All of the messages in the chat history

    :param chat_history: The Chat History for the Messenger Chat
    :return: The List of Messages in the chat
    """
    return chat_history.ChatMessages


def messages_by_participant(chat_history: ChatHistory, participant: str) -> list:
    """
    Fetches all of the messages sent by a given participant

    :param chat_history: The Chat History for the Messenger Chat
    :param participant: The string of a participant
    :return: The list of messages for the given participant
    """
    return chat_history.ChatParticipants[participant].Messages


def _message_time_period(message_list: list, min_time: datetime.datetime, max_time: datetime.datetime) -> list:
    """
    Fetches all of the messages within a given time period from a list of messages

    :param message_list:
    :param min_time: The farthest back to check
    :param max_time: The soonest to check
    :return: The list of messages in the given time period
    """
    fit_criteria = []

    for msg in message_list:
        if min_time <= msg.timestamp <= max_time:
            fit_criteria.append(msg)
    return fit_criteria


def messages_per_time_period(chat_history: ChatHistory,
                             min_time: datetime.datetime,
                             max_time: datetime.datetime) -> list:
    """
    Fetches all of the messages within a given time period from the Chat History

    :param chat_history: The Chat History for the Messenger Chat
    :param min_time: The farthest back to check
    :param max_time: The soonest to check
    :return: The list of messages in a given time period
    """
    chat_messages = chat_history.ChatMessages
    fit_criteria = _message_time_period(chat_messages, min_time, max_time)

    return fit_criteria


def messages_per_time_period_per_person(chat_history: ChatHistory,
                                        min_time: datetime.datetime,
                                        max_time: datetime.datetime,
                                        participant: str) -> list:
    """
    Fetches all of the messages within a given time period sent by a given participant

    :param chat_history: The Chat History for the Messenger Chat
    :param min_time: The farthest back to check
    :param max_time: The soonest to check
    :param participant: The string name of a participant
    :return: A list of messages
    """
    participant_messages = messages_by_participant(chat_history, participant)

    return _message_time_period(participant_messages, min_time, max_time)
