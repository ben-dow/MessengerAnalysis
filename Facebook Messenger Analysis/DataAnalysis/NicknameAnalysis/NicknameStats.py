import matplotlib.pyplot as pl
from DataBuilder.MessageInformation import ChatHistory


def most_nicknames(chat_history: ChatHistory) -> None:
    """
    WORK IN PROGRESS

    Graphs the Number of Nicknames Each participant has had
    :param chat_history: The Chat History

    """
    names = chat_history.ChatParticipants.keys()

    x = range(len(names))
    y = []

    for p in names:
        num_nicks = len(chat_history.ChatParticipants[p].Nicknames)
        y.append(num_nicks)

    ys, ns = zip(*sorted(zip(*(y, names))))

    pl.barh(x, ys)
    pl.yticks(x, ns)
    pl.axes().grid()
    pl.xticks(y, y)
    pl.title("Which gugs have had the most nicknames?")
    pl.show()
