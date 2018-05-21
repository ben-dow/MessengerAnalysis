"""
Functions to return lists of Messages based on criteria
Created by Benji Dow on 5/19/2018
"""


def all_messages(chat_history):
    return chat_history.ChatMessages


def messages_by_participant(chat_history, participant):
    return chat_history.ChatParticipants[participant].Messages


# Helper Function to get messages from a message list within a time period
def _message_time_period(message_list, min, max):
    fit_criteria = []

    for msg in message_list:
        if min <= msg.timestamp <= max:
            fit_criteria.append(msg)
    return fit_criteria


def messages_per_time_period(chat_history, min, max):
    # Get Iterator of Messages
    chat_messages = chat_history.ChatMessages
    fit_criteria = _message_time_period(chat_messages,min, max)

    return fit_criteria


def messages_per_time_period_per_person(chat_history, min, max, participant):
    participant_messages = messages_by_participant(chat_history, participant)

    return _message_time_period(participant_messages, min, max)
