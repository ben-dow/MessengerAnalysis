import json
import time

from DataBuilder.ChatParsing import ChatHistory

'''
print("What is the Location of the File?")
file_location = input()

print("What is the full facebook name of the user that downloaded this data?")
data_owner = input()
'''
file_location = "C:\\Users\Benjamin Dow\Desktop\BAEtchyasevah_732c7ad1d8\message.json"
data_owner = "Benjamin Dow"

with open(file_location) as file:
    data = json.load(file)

start = time.time()
chat = ChatHistory(data, data_owner, True, True, True)
print(time.time() - start)

for p in chat.ChatParticipants:
    print(p + ": ")
    names = []
    for n in chat.ChatParticipants[p].Nicknames.keys():
        names.append(n)
    print(names.__str__() + '\n')

'''
Do Analysis on it Down Here:
'''




