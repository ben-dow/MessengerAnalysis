def nicknames_for_person(chat_history, Participant):

    if Participant in chat_history.ChatParticipants:
        return chat_history.ChatParticipants[Participant].Nicknames
