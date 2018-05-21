import matplotlib.pyplot as pl
import itertools

def most_nicknames(chat_history):

    names = chat_history.ChatParticipants.keys()

    x = range(len(names))
    y = []

    for p in names:
        numnick =len(chat_history.ChatParticipants[p].Nicknames)
        y.append(numnick)

    ys, ns = zip(*sorted(zip(*(y, names))))

    pl.barh(x, ys)
    pl.yticks(x,ns)
    pl.axes().grid()
    pl.xticks(y,y)
    pl.title("Which gugs have had the most nicknames?")
    pl.show()





