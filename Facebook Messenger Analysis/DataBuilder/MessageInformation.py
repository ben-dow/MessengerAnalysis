import datetime



class ChatHistory(object):

    def __init__(self, JsonData, DataOwner):

        self.DataOwner = DataOwner
        self.ChatParticipants = self.process_participant_list(JsonData["participants"])
        self.ChatMessages = self.process_messages(JsonData["messages"])

        from DataBuilder.NicknameParsing import reconstruct_nicknames
        reconstruct_nicknames(self)


    @staticmethod
    def process_participant_list(participant_json):
        participant_list = {}
        for p in participant_json:
            participant_list[p] = Participant(p)
        return participant_list

    def process_messages(self, message_json):

        msgs = []
        for m in message_json:

            msg = Message(m)
            msgs.append(msg)

            if msg.Sender not in self.ChatParticipants:
                self.ChatParticipants[msg.Sender] = Participant(msg.Sender)

            self.ChatParticipants[msg.Sender].Messages.append(msg)

        return msgs

    def __str__(self):
        participant_num = self.ChatParticipants.__len__()
        message_num = self.ChatMessages.__len__()

        return "Number of Participants: " + participant_num.__str__() \
               + '\n' + "Number of Messages: " + message_num.__str__()


class Participant(object):

    def __init__(self, name):
        self.Name = name
        self.Messages = []
        self.Nicknames = []
        self.Reactions = []

    def number_of_messages(self):
        return len(self.Messages)


class Nickname(object):

    def __init__(self, participant_name, setter_name, timestamp, nickname):
        self.ParticipantName = participant_name
        self.SetterName = setter_name
        self.timestamp = timestamp
        self.Nickname = nickname

    def __str__(self):
        return_str = self.SetterName + " set " +\
                     self.ParticipantName + "'s nickname to " +\
                     self.Nickname + " on " +\
                     self.timestamp.__str__()
        return return_str


class Message(object):
    def __init__(self, message_data):

        self.Sender = message_data["sender_name"]

        self.timestamp = datetime.datetime.\
            fromtimestamp(int(message_data["timestamp"]))

        self.Type = message_data["type"]

        self.Content, self.ContentType = self.process_message_content(message_data)

        self.ReactData = self.process_message_reactions(message_data)

    def __str__(self):
        str = "Sender: " + self.Sender + '\n' + \
              "Timestamp: " + self.timestamp.__str__() + '\n' + \
              "Message: " + self.Content.__str__() + '\n'
        return str

    @staticmethod
    def process_message_content(message_data):

        # Process Message that contained Photos
        if "photos" in message_data:
            content_type = "PHOTOS"
            content = []
            for p in message_data["photos"]:
                content.append(p["uri"])

        # Process Message that contained gifs
        elif "gifs" in message_data:
            content_type = "GIFS"
            content = []
            for g in message_data["gifs"]:
                content.append(g["uri"])

        # Process Message that contained text content
        # TODO Process messages that actually are a function within the chat
        # TODO Such as Polls, Nicknames, or Adding Someone to the Chat
        elif "content" in message_data:
            content_type = "MESSAGE"
            content = message_data["content"]

        # Process Message that contained stickers
        elif "sticker" in message_data:
            content_type = "STICKER"
            content = message_data["sticker"]["uri"]

        # Process Message that contained Files
        elif "file" in message_data:
            content_type = "FILE"
            content = []
            for f in message_data["files"]:
                content.append(f["uri"])
        # Process Message that contained No type of Content in the JSON
        else:
            content_type = "NONE"
            content = None

        return content, content_type

    @staticmethod
    def process_message_reactions(message_data):

        if "reactions" in message_data:
            react_data = []
            for r in message_data["reactions"]:
                reaction =  r["reaction"]
                actor = r["actor"]
                react_data.append((reaction,actor))

        else:
            react_data = None

        return react_data










