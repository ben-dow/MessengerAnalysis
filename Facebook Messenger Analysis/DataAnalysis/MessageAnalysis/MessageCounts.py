from DataAnalysis.MessageAnalysis.MessageLists import *
from DataBuilder.MessageInformation import ChatHistory

"""
Methods to return counts of messages based on criteria
"""


def total_messages(chat_history: ChatHistory) -> int:
    """

    :param chat_history: The Chat History for the Messenger Chat
    :return: The Number of Messages sent in the chat
    """
    return len(chat_history.ChatMessages)


def total_participants(chat_history: ChatHistory) -> int:
    """

    :param chat_history: The Chat History for the Messenger Chat
    :return: The count of the total number of participants in the chat
    """
    return len(chat_history.ChatParticipants)


def messages_count_per_participant(chat_history: ChatHistory) -> dict:
    """

    :param chat_history: The Chat History for the Messenger Chat
    :return: The dictionary containing message counts for all participants
    """
    message_count = {}
    for p in chat_history.ChatParticipants:
        message_count[p] = chat_history.ChatParticipants[p].number_of_messages()
    return message_count


def num_messages_in_time_period(chat_history: ChatHistory,
                                min_date: datetime.datetime,
                                max_date: datetime.datetime) -> int:
    """

    :param chat_history: The Chat History for the Messenger Chat
    :param min_date: The Minimum date for message
    :param max_date:  The Maximum date for messages
    :return: The number of messages in that time
    """
    return len(messages_per_time_period(chat_history, min_date, max_date))


