import re


class Poll(object):
    pass


class PollVote(object):
    pass


def poll_messages(message_list: list) -> list:

    poll_creation_regex = re.compile('.* created a poll: .*')  # Creation of a Poll

    poll_vote_regex = re.compile('.* voted for .* in the poll: .*')  # Voted in the poll

    poll_vote_removed_regex = re.compile('.* removed vote for .* in the poll: .*')  # Removal of a vote in a poll


