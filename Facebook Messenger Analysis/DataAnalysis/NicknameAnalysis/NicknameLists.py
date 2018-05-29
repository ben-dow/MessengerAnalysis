from DataBuilder.MessageInformation import ChatHistory


def nicknames_for_person(chat_history: ChatHistory, participant: str) -> list:
    """
    Fetches all of the nicknames for a given person name from the chat history

    :param chat_history: The chat history for the Messenger Chat
    :param participant: The participant string
    :return: A list of the nicknames
    """
    if participant in chat_history.ChatParticipants:  # Makes sure the participant exists
        return chat_history.ChatParticipants[participant].Nicknames


def nicknames_by_participant(chat_history: ChatHistory) -> dict:
    """
    Fetches all of the nicknames for all of the participants in the chat and returns it as a dict
    :param chat_history: the chat history
    """
    res = {}

    for p in chat_history.ChatParticipants:
        nicks = chat_history.ChatParticipants[p].Nicknames
        for n in nicks:
            res[p] = nicks[n].Nickname

    return res