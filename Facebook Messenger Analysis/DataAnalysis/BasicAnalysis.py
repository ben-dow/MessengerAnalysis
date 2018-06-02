from DataAnalysis.MessageAnalysis.MessageCounts import total_messages, total_participants, \
    messages_count_per_participant
from DataAnalysis.NicknameAnalysis.NicknameLists import nicknames_by_participant
from DataBuilder.ChatParsing import ChatHistory


def basic_analysis_package(chat: ChatHistory) -> dict:
    res = {
        "Total Messages": total_messages(chat),
        "Total Participants": total_participants(chat),
        "Message Counts By Participants": messages_count_per_participant(chat),
        "Nicknames for Each Participant": nicknames_by_participant(chat),
        "Chat Name": chat.ChatName,
        "Data Owner:": chat.DataOwner
    }
    return res
