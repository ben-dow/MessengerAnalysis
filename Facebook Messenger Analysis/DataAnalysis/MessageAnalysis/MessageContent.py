from DataBuilder.MessageInformation import ChatHistory


def word_count(word: str, chat_history: ChatHistory = None, message_list: list = []) -> int:
    """
    Counts the occurrences of a word in a Chat History or message list

    :param word: The Word to Be Counted
    :param chat_history: A chat history for a messenger conversation
    :param message_list: A list of message
    :return: The integer count of words in the given messages
    """

    count = 0  # Initiate Count

    if chat_history is not None:  # If Chat history is given set the message list from that history
        message_list = chat_history.ChatMessages

    for m in message_list:
        if m.Content is not None and\
                word in m.Content.__str__().lower():  # Make Sure message has content and make it lowercase
            count += 1
    return count

