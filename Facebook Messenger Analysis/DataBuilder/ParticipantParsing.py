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


def _process_participant_list(participants_list: list) -> dict:
        """
        Processes the JSON Data of Participants into a list of Participant Objects that can be manipulated

        :param participants_list: The list of participants from the JSON Data
        :return: A list of Participant Objects
        """
        participant_list = {}  # Initiate Dictionary to Store Participants

        for p in participants_list:
            participant_list[p["name"]] = Participant(p["name"])

        return participant_list