class ChatHistory(object):
    """

    Describes and holds all of the data for a Chat History parsed from a Facebook Messenger JSON
    Currently Processes:
        Chat Participants
        Chat Messages
        Nicknames

    It requires the manual input of the Full Facebook Name of the User who Downloaded the JSON from FB


    """

    def __init__(self, json_data: dict, data_owner: str, nicknames:bool = False, membership_history:bool = False, chat_names_history: bool = False) -> None:
        """
        Initiates the Chat History Object

        :param json_data: The dictionary containing all of the JSON data for the messenger
        :param data_owner: The string for the name of the data owner
        """
        self.DataOwner = data_owner
        self.ChatName = json_data["title"]
        self.ChatNameHistory = []

        '''Basic Analysis'''
        from DataBuilder.ParticipantParsing import _process_participant_list
        self.ChatParticipants = _process_participant_list(json_data["participants"])

        from DataBuilder.MessageParsing import _process_messages
        self.ChatMessages = _process_messages(json_data["messages"], self)


        '''Extra Analysis'''
        if nicknames or membership_history or chat_names_history: # If the other extra is wanted then nicknames has to be executed because it is used in the parsing
            from DataBuilder.NicknameParsing import reconstruct_nicknames
            reconstruct_nicknames(self)
        if membership_history:
            from DataBuilder.MemberShipParsing import person__added_or_removed__reconstruction
            person__added_or_removed__reconstruction(self)
        if chat_names_history:
            from DataBuilder.ChatNameParsing import chat_renamed_reconstruction
            chat_renamed_reconstruction(self)

    def __str__(self) -> str:
        """
        Creates a String representation of the Chat History
        :return: A String of the Chat History
        """
        participant_num = self.ChatParticipants.__len__()
        message_num = self.ChatMessages.__len__()

        return "Number of Participants: " + participant_num.__str__() \
               + '\n' + "Number of Messages: " + message_num.__str__()
