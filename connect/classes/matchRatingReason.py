class MatchRatingReason:
    def __init__(self,subjectFacebookID,objectFacebookID,reason):
        self.subject = subjectFacebookID
        self.object = objectFacebookID
        self.reason = reason


    def __str__( self ):
        return "subject: %s  object: %s reason: %s" % ( self.subject, self.object,self.reason)