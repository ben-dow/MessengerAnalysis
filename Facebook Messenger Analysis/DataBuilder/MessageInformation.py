import datetime


class ChatHistory(object):
    """

    Describes and holds all of the data for a Chat History parsed from a Facebook Messenger JSON
    Currently Processes:
        Chat Participants
        Chat Messages
        Nicknames

    It requires the manual input of the Full Facebook Name of the User who Downloaded the JSON from FB


    """

    def __init__(self, json_data: dict, data_owner: str) -> None:
        """
        Initiates the Chat History Object

        :param json_data: The dictionary containing all of the JSON data for the messenger
        :param data_owner: The string for the name of the data owner
        """
        self.DataOwner = data_owner
        self.ChatParticipants = self._process_participant_list(json_data["participants"])
        self.ChatMessages = self._process_messages(json_data["messages"])
        self.ChatName = json_data["title"]
        self.ChatNameHistory = []

        from DataBuilder.NicknameParsing import reconstruct_nicknames
        reconstruct_nicknames(self)

        from DataBuilder.MemberShipParsing import person__added_or_removed__reconstruction
        person__added_or_removed__reconstruction(self)

        from DataBuilder.ChatNameParsing import chat_renamed_reconstruction
        chat_renamed_reconstruction(self)

    @staticmethod
    def _process_participant_list(participants_list: list) -> dict:
        """
        Processes the JSON Data of Participants into a list of Participant Objects that can be manipulated

        :param participants_list: The list of participants from the JSON Data
        :return: A list of Participant Objects
        """
        participant_list = {}  # Initiate Dictionary to Store Participants

        for p in participants_list:
            participant_list[p] = Participant(p)

        return participant_list

    def _process_messages(self, message_list: list) -> list:
        """
        Processes the Messages form the JSON Data into a list of Message Objects that can be manipulated

        :param message_list: A list of Messages from the JSON Data
        :return: A list of Message Objects
        """
        msgs = []
        for m in message_list:

            msg = Message(m)
            msgs.append(msg)

            if msg.Sender not in self.ChatParticipants:  # Check if the Sender is a Participant
                self.ChatParticipants[msg.Sender] = Participant(msg.Sender)  # Add the Sender to the Participant List

            self.ChatParticipants[msg.Sender].Messages.append(msg)

        return msgs

    def __str__(self) -> str:
        """
        Creates a String representation of the Chat History
        :return: A String of the Chat History
        """
        participant_num = self.ChatParticipants.__len__()
        message_num = self.ChatMessages.__len__()

        return "Number of Participants: " + participant_num.__str__() \
               + '\n' + "Number of Messages: " + message_num.__str__()


class Participant(object):

    def __init__(self, name: str) -> None:
        """
        Initiates a Participant Object which contains the data for a participant in the messenger chat

        :param name: The String Name of the Participant
        """
        self.Name = name
        self.Messages = []
        self.Nicknames = {}
        self.Reactions = []
        self.MemberShipRecords = []

    def number_of_messages(self) -> int:
        """
        Calculates the number of messages that the participant has sent

        :return: The Integer of the number of messages sent by the participant
        """
        return len(self.Messages)


class Message(object):
    def __init__(self, message_data: dict) -> None:
        """
        Initiates a Message Object which contains the data for a Message that was sent in a Messenger Chat
        from the raw JSON Data

        :param message_data: The JSON Data for a Message from Facebook
        """
        self.Sender = message_data["sender_name"]

        self.timestamp = datetime.datetime. \
            fromtimestamp(int(message_data["timestamp"]))

        self.Type = message_data["type"]

        self.Content, self.ContentType = self.process_message_content(message_data)

    def __str__(self) -> str:
        """
        Creates a string representation of a Message object

        :return: The string representation
        """
        return_str = "Sender: " + self.Sender + '\n' + \
              "Timestamp: " + self.timestamp.__str__() + '\n' + \
              "Message: " + self.Content.__str__() + '\n'
        return return_str

    @staticmethod
    def process_message_content(message_data: dict) -> (str or list, str):
        """
        Function to process the message content from the JSON (dict) Data
        :param message_data: The JSON Data
        :return: A tuple containing a string of Content or the list of content sent and a str describing what kind of message it is
                The message could be one of the following:
                PHOTOS
                GIFS
                MESSAGE
                FILE
        """
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
