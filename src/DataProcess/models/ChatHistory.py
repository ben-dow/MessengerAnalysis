from typing import Dict, Any

from DataProcess.models.Person import Person
from DataProcess.models.Message import Message


class ChatHistory(object):
    People: Dict[str, Person]

    def __init__(self):
        self.Messages = []  # Message Objects
        self.People = {}  # Display Name ==> People Object
        self.NicknameLookup = {}  # Nickname ==> Person Object

    def add_message(self, raw_message):
        msg = Message.message_creator(raw_message, self)
        self.Messages.append(msg)

        # Account for People
        if msg.sender_name not in self.People:
            self.add_person(msg.sender_name)

        self.People[msg.sender_name].Messages.append(msg)

    def add_person(self, sender_name):
        self.People[sender_name] = Person(sender_name)

    def get_person(self, name):
        if name in self.People:
            return self.People.get(name)

        self.add_person(name)
        return self.People.get(name)
