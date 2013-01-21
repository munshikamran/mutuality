class MeetPeopleProfile:
    def __init__(self,facebookUser):
        attributes = ["gender","relationshipStatus","college","age","location","employer"]
        defaultAttrVal = ""
        for attr in attributes:
            attrVal = getattr(facebookUser,attr,defaultAttrVal)
            print attrVal
            setattr(self,attr,attrVal)