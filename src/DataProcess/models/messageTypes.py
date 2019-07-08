messageTypes = ['AddMember',
                'RemoveMember',
                'LeaveMember',
                'Generic',
                'OtherNicknameSet',
                'SelfNicknameSet',
                'ThisSelfNicknameSet',
                'ThisOtherNicknameSet'
                'CreatePoll',
                'PollVote']

regexExpressions = {
    'OtherNicknameSet': '^(.*) set (?:the nickname for (.*?)|(your) nickname) to (.*).$',
    'SelfNicknameSet': '^.* set (her | his | their| your)own nickname to .*\\.$',
}
