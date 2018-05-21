"""
Methods to return counts of messages based on criteria
"""

# Get the Total Number of Message Sent in the Chats
from DataAnalysis.MessageAnalysis.MessageLists import *


def total_messages(chat_history):
    return len(chat_history.ChatMessages)


def total_participants(chat_history):
    return len(chat_history.ChatParticipants)


def messages_count_per_participant(chat_history):
    message_count = {}
    for p in chat_history.ChatParticipants:
        message_count[p] = chat_history.ChatParticipants[p].number_of_messages()
    return message_count


def num_messages_in_time_period(chat_history, min, max):
    return len(messages_per_time_period(chat_history, min, max))


