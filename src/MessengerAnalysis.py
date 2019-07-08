from pprint import pprint

from DataProcess import ProcessMessageFile
from DataProcess.models.Message import AddMember, RemoveMember, LeaveMember

chat_history = ProcessMessageFile.process_message_file(None)


f = open("Stats.txt", "w+")

f.write("\t#" * 9)
f.write("\n\t\t\t\tGUGS!\n")
f.write("\t#" * 9)
f.write("\n")
f.write("\n")


f.write("Total Participants (ever): " + str(len(chat_history.People.values())))
f.write("\n")
f.write("Total Message Sent: " + str(len(chat_history.Messages)))

most_message = ("name", 0)
most_nicks = ("name", 0)
all =[]
most_set = ("name", 0)
for p in chat_history.People.values():
    all.append((p.DisplayName, len(p.Messages)))

    if len(p.Messages) > most_message[1]:
        most_message = (p.DisplayName, len(p.Messages))

    if len(p.Nicknames) > most_nicks[1]:
        most_nicks = (p.DisplayName, len(p.Nicknames))

    num_set = 0
    for n in chat_history.NicknameLookup.values():
        if n.setter == p:
            num_set += 1

sorted_by_second = sorted(all, key=lambda tup: tup[1], reverse=True)


f.write("\n\nMost Messages: " + most_message[0])
f.write("\n\t# Messages: " + str(most_message[1]))

f.write("\n\nTop 5")
for i in range(0,10):
    f.write("\t\t\n" + str(sorted_by_second[i]))

f.write("\n\nMost Nicknames: " + most_nicks[0])
f.write("\n\t# Nicknames: " + str(most_nicks[1]))

f.write("\n\nMost Nicknames Set: " + most_set[0])
f.write("\n\t# Nicknames Set: " + str(most_set[1]))


f.write("\n")
f.write("\n")
f.write("#" * 14)
f.write("\nALL THE PEEPS\n")
f.write("#" * 14)

for p in chat_history.People.values():
    f.write("\n\nName: " + p.DisplayName)
    f.write("\n\tMessages Sent: " + str(len(p.Messages)))

    adds = 0
    remove = 0
    leave = 0
    for m in p.Messages:
        if isinstance(m, AddMember):
            adds += 1
        if isinstance(m, RemoveMember):
            remove += 1
        if isinstance(m, LeaveMember):
            leave += 1

    f.write("\n\t# of People Added: " + str(adds))
    f.write("\n\t# of People Removed: " + str(remove))
    f.write("\n\t# of Leaves: " + str(leave))


    num_set = 0
    for n in chat_history.NicknameLookup.values():
        if n.setter == p:
            num_set += 1
    f.write("\n\t# Nicknames Set: " + str(num_set))

    f.write("\n\t# Nicknames: " + str(len(p.Nicknames)))
    f.write("\n\tNicknames:")
    for n in p.Nicknames:
        f.write("\n\t\t"+n.nickname)


