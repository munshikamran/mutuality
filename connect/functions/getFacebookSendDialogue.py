import settings

def GetFacebookSendDialogue(profile,facebookUser,redirect_uri,link,description):
    urlRoot = 'https://www.facebook.com/dialog/send?'
    prop = {}
    prop['app_id'] = settings.FACEBOOK_APP_ID
    prop['redirect_uri'] = redirect_uri
    prop['to'] = facebookUser.facebookID
    prop['link'] = link
    prop['description'] = description
    url = urlRoot
    keys = prop.keys()
    for key in keys[0:len(keys)-1]:
        url +=  key + '=' + prop[key] + '&'
    key = keys[-1]
    url += key + '=' + prop[key]
    return url