class MeetPeopleResponse:
    def __init__(self,freshUsers,viewedUsers):
#        new users are ordered by number of mutual friends. The user with the most mutual friends with
#        the requesting user is first in the list
        self.freshUsers = freshUsers
#        viewed users are ordered by how recently the user was viewed. The user who was viewed most
#        recently by the requesting user is first in the list
        self.viewedUsers = viewedUsers