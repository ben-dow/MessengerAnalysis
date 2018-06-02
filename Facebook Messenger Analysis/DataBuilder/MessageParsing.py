import datetime

from DataBuilder.ParticipantParsing import Participant
from DataBuilder.ChatParsing import ChatHistory

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


def _process_messages(message_list: list, chat_history: ChatHistory) -> list:
        """
        Processes the Messages form the JSON Data into a list of Message Objects that can be manipulated

        :param message_list: A list of Messages from the JSON Data
        :return: A list of Message Objects
        """
        msgs = []
        for m in message_list:

            msg = Message(m)
            msgs.append(msg)

            if msg.Sender not in chat_history.ChatParticipants:  # Check if the Sender is a Participant
                chat_history.ChatParticipants[msg.Sender] = Participant(msg.Sender)  # Add the Sender to the Participant List

            chat_history.ChatParticipants[msg.Sender].Messages.append(msg)

        return msgs