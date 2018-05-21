import json

from DataBuilder.MessageInformation import ChatHistory

print("What is the Location of the File?")
file_location = input()

print("What is the full facebook name of the user that downloaded this data?")
data_owner = input()

with open(file_location) as file:
    data = json.load(file)

chat = ChatHistory(data,data_owner)

'''
Do Analysis on it Down Here:
'''


