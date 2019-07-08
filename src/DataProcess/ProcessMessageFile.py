import pprint
import json

from DataProcess.models.ChatHistory import ChatHistory
from DataProcess.models.Message import Message
from DataProcess.models.Person import Person


def process_message_file(filename):
    # Get File
    filename = ""
    file = open(filename)
    jsonFile = json.load(file)

    # Storage Class
    chat_history = ChatHistory()

    # Process People
    rawPeople = jsonFile["participants"]

    for rawPerson in rawPeople:
        chat_history.add_person(rawPerson["name"])

    # Process Messages
    raw_messages = jsonFile["messages"]
    for raw_message in raw_messages:
        chat_history.add_message(raw_message)

    return chat_history
