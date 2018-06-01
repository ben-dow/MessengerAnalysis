import json
import time

from DataBuilder.MessageInformation import ChatHistory

'''
print("What is the Location of the File?")
file_location = input()

print("What is the full facebook name of the user that downloaded this data?")
data_owner = input()
'''
file_location = "C:\\Users\Benjamin Dow\Desktop\GugsnTwelce_f0e495bd93\message.json"
data_owner = "Benjamin Dow"

with open(file_location) as file:
    data = json.load(file)

start = time.time()
chat = ChatHistory(data, data_owner)
print(time.time() - start)

for n in chat.ChatNameHistory:
    print(n)

'''
Do Analysis on it Down Here:
'''




