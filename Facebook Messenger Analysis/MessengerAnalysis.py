import json
import time

from DataAnalysis.MembershipAnalysis.RemovedAnalysis import most_removed
from DataAnalysis.MessageAnalysis.MessageCounts import messages_count_per_participant
from DataBuilder.MessageInformation import ChatHistory


print("What is the Location of the File?")
file_location = input()

print("What is the full facebook name of the user that downloaded this data?")
data_owner = input()


with open(file_location) as file:
    data = json.load(file)

start = time.time()
chat = ChatHistory(data,data_owner)
print(time.time() - start)
'''
Do Analysis on it Down Here:
'''