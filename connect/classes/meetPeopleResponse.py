class MeetPeopleResponse:
    SUCCESS_MESSAGE = 'success'
    SEEN_ALL_MATCHES_MESSAGE = 'you have seen all potential matches'
    NO_FRIENDS_MESSAGE = 'you have no friends on the site'
    UNKNOWN_ERROR_MESSAGE = 'an unknown error occurred'
    def __init__(self, potentialMatches, message):
#        new users are ordered by number of mutual friends. The user with the most mutual friends with
#        the requesting user is first in the list
        self.potentialMatches = potentialMatches
