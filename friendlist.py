import json
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import datetime
from datetime import timedelta
import SteamObjects


#!/usr/bin/python

#datetime.datetime.fromtimestamp()
#unix to stamp


#to do
#her hesap için farklı klasöre kayıt et
#her ay yıl içi içinde bir kalsöere kayıt et
#f.writelines(f'Picture: \n')#to doo
#f.writelines(f'URL: \n')#to doo
#steam normal linkten 64 id yi çek




key = '028C52FB094CC5AD399D2835C3E97964'



def access_friendlist(steamid):
    friendsList = []

    linkArgs = {'key': key, 'steamid': steamid, 'relationship': 'friend'}
    encodedArgs = urllib.parse.urlencode(linkArgs)

    link = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?' + encodedArgs
    data = json.load(urllib.request.urlopen(link))

    results = data['friendslist']['friends']

    for r in results:
        friend = SteamObjects.FriendList()

        friend.steamid = r.get('steamid')
        friend.relationship = r.get('relationship')
        friend.friend_since = datetime.datetime.fromtimestamp(int(r.get('friend_since', 0)))
        friend.friend_sinceunix = r.get('friend_since', 0)

        friendsList.append(friend)


    return friendsList


def get_user_name(steamid):
    linkArgs = {'key': key, 'steamids': steamid}
    encodedArgs = urllib.parse.urlencode(linkArgs)

    link = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?' + encodedArgs

    data = json.load(urllib.request.urlopen(link))

    result = data['response']['players'][0]['personaname']
    return result


def get_user_names(steamids):
    usernames = []

    #print ",".join(steamids)

    linkArgs = {'key': key, 'steamids': ",".join(steamids)}
    encodedArgs = urllib.parse.urlencode(linkArgs)

    link = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?' + encodedArgs

    data = json.load(urllib.request.urlopen(link))

    results = data['response']['players']

    #loop through results and add each personaname to the list
    for u in results:
        usernames.append(u['personaname'].strip())

    return usernames


def get_user_info(steamid):
    user = SteamObjects.PlayerSummary()

    linkArgs = {'key': key, 'steamids': steamid}
    encodedArgs = urllib.parse.urlencode(linkArgs)

    link = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?' + encodedArgs

    data = json.load(urllib.request.urlopen(link))

    playerInfo = data['response']['players']

    for p in playerInfo:
        user.steamid = p.get('steamid')
        user.communityvisibilitystate = p.get('communityvisibilitystate', 1)
        user.profilestate = p.get('profilestate', 0)
        user.personaname = p.get('personaname')
        try:
            user.lastlogoff=datetime.datetime.fromtimestamp(int(p.get('lastlogoff', 0)))
        except:
            user.lastlogoff= ''
        #user.lastlogoff = datetime.datetime.fromtimestamp(int(p.get('lastlogoff', 0)))

        user.lastlogoffunix = p.get('lastlogoff', 0)
        user.profileurl = p.get('profileurl')
        user.avatar = p.get('avatar')
        user.avatarmedium = p.get('avatarmedium')
        user.avatarfull = p.get('avatarfull')
        user.personastate = p.get('personastate', 0)
        user.primaryclanid = p.get('primaryclanid')
        user.timecreatedunix = p.get('timecreated', 0)
        user.personastateflags = p.get('personastateflags')

        state = user.personastate

        if state == 0:
            user.personastatetext = "Offline"
        elif state == 1:
            user.personastatetext = "Online"
        elif state == 2:
            user.personastatetext = "Busy"
        elif state == 3:
            user.personastatetext = "Away"
        elif state == 4:
            user.personastatetext = "Snooze"
        elif state == 5:
            user.personastatetext = "Looking to trade"
        elif state == 6:
            user.personastatetext = "Looking to play"
        else:
            user.personastatetext = ""

        visibility = user.communityvisibilitystate

        if visibility == 1:
            user.communityvisibilitystate = 'Private (1)'
        elif visibility == 2:
            user.communityvisibilitystate = 'Private (2)'
        elif visibility == 3:
            user.communityvisibilitystate = 'Public (3)'
        else:
            user.communityvisibilitystate = user.communityvisibilitystate

    return user

steamid = str(input('Please enter your 64 bit Steam ID here: ')).strip()


while not steamid.isdigit():
    print('That is not a valid Steam ID')
    steamid = str(input('Please enter your 64 bit Steam ID here: ')).strip()


now = datetime.datetime.now()
yesterday = timedelta(hours=24)
diff = now - yesterday


try:
    friends = access_friendlist(steamid)
except:

    print('Profile name: '+get_user_name(steamid))
    print('This profile is private.I can\'t see the friend list.')
    exit()


username = get_user_name(steamid)

#userFilter = input("Please enter first character of username you'd like to filter or leave empty for all results: ").strip()

friendCounter=1
for friendObj in friends:


    # logOff = get_user_logoff(r)

    userInfo = get_user_info(friendObj.steamid)

    print(friendCounter)
    print(userInfo.steamid + ": " + userInfo.personaname)
    print('Picture: '+ userInfo.avatarfull)
    print("Last logged off: " + str(userInfo.lastlogoff))
    #print('Time created unix: '+ str(userInfo.timecreatedunix))
    #print('Persona state flags: '+ str(userInfo.personastateflags))
    #print('Avatar medium: '+ userInfo.avatarmedium)
    #print('Primary clan id: '+ userInfo.primaryclanid)
    #print('avatar: '+ userInfo.avatar)
    print('lastlogoffunix: '+ str(userInfo.lastlogoffunix))
    #print('profilestate: '+ str(userInfo.profilestate))
    print('Visibility state: '+ str(userInfo.communityvisibilitystate))
    print("Status: " + userInfo.personastatetext)
    print("Profile URL: " + userInfo.profileurl)
    print("Friend since: " + str(friendObj.friend_since))
    print()
    print("---------------------")
    print()


    f = open(f'({now.hour}-{now.minute}-{now.second})-({now.day}-{now.month}-{now.year})-{username}-{len(friends)}.txt','a+',encoding="utf-8")

    f.writelines(f'{friendCounter}\n')
    try:
        f.writelines('Steam name: '+userInfo.personaname + '\n')
    except:
        f.writelines(f'\n')
    f.writelines('Last logged off: '+str(userInfo.lastlogoff) + '\n' )
    f.writelines('Last log off unix: '+ str(userInfo.lastlogoffunix) + '\n' )
    f.writelines('Steam Id: '+userInfo.steamid + '\n')
    f.writelines('Picture: '+ userInfo.avatarfull+ '\n')
    f.writelines('Visibility : '+ str(userInfo.communityvisibilitystate)+ '\n')
    f.writelines("Status: " + userInfo.personastatetext+ '\n')
    f.writelines("Profile URL: " + userInfo.profileurl+ '\n')
    f.writelines("Friend since: " + str(friendObj.friend_since)+ '\n')
    f.writelines("------------------------------------\n")
    friendCounter+=1

    # if userInfo.personaname.startswith(userFilter) and userInfo.lastlogoff > diff:
    #     print userInfo.personaname + " " + "last logged off at " + str(userInfo.lastlogoff) + " with steamid: " + userInfo.steamid

f.writelines('My Any infos: \n')
f.writelines(f'nName: {username}\n')
f.writelines(f'Picture: \n')#to doo
f.writelines(f'URL: \n')#to doo
f.writelines(f'Link: https://steamcommunity.com/profiles/{steamid}/\n')
f.writelines(f'Friends : {len(friends)}\n')
f.writelines(f'Current Time: {now}\n')

f.close()



