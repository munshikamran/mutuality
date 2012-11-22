from connect.models import FacebookUser
class FriendMatch:
    def __init__(self,person1,person2):
        self.person1 = person1
        self.person2 = person2

        self.matchCriteria = []
        if self.person1.location == self.person2.location:
            self.matchCriteria.append('sameLocation')
        elif self.person1.state == self.person2.state:
            self.matchCriteria.append('sameState')

    def __str__( self ):
        return "%s  %s" % ( self.person1.name, self.person2.name)