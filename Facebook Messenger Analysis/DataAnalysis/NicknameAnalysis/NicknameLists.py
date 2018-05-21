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
