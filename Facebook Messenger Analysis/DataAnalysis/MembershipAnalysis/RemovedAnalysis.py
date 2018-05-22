from DataBuilder.MessageInformation import ChatHistory


def most_removed(chat_history:ChatHistory):

    removals = []

    for p in chat_history.ChatParticipants:
        count = 0
        for m in chat_history.ChatParticipants[p].MemberShipRecords:
            if m.RecordType == "REMOVED":
                count += 1
        removals.append((p,count))

    removals.sort(key=lambda x: x[1])
    return removals
