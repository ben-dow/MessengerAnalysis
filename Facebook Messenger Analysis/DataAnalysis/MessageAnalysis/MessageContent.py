from DataBuilder.MessageInformation import ChatHistory,Message


def word_count(word, chat_history = None, message_list = []):
    count = 0
    if chat_history is not None:
        message_list = chat_history.ChatMessages

    for m in message_list:
        if m.Content is not None and word in m.Content.__str__().lower():
            count += 1
    return count

