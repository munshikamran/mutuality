class MeetPeopleProfile:
    def __init__(self,facebookUser):
        attributes = ["name","gender","relationshipStatus","college","age","location","employer"]
        defaultAttrVal = ""
        for attr in attributes:
            attrVal = getattr(facebookUser,attr,defaultAttrVal)
            setattr(self,attr,attrVal)