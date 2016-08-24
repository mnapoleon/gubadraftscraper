import re, requests, bs4, slackclient, time

SLACK_TOKEN = ''

def getTeamIcon(teamName):
    teams = {
        'Bison' : ':bei:',
        'Toros' : ':bog:',
        'Albicelestes' : ':ba:',
        'Pharaohs' : ':cai:',
        'Hooks' : ':cc:',
        'Crusaders' : ':chc:',
        'Bears' : ':den:',
        'Kernels' : ':dm:',
        'Shamrocks' : ':dub:',
        'Prospectors' : ':elp:',
        'Moonshiners' : ':gre:',
        'Island Kings' : ':hon:',
        'Orbits' : ':hou:',
        'Tidal Wave' : ':jak:',
        'Monarchs' : ':kc:',
        'Dragons' : ':kra:',
        'Spitfires' : ':lon:',
        'Express' : ':la:',
        'Enforcers' : ':mos:',
        'Sounds' : ':nas:',
        'Knights' : ':ny:',
        'Brewers': ':phi:',
        'Outlaws' : ':san:',
        'Tiburones' : ':sj:',
        'Tortugas' : ':sd:',
        'Oncas' : ':sao:',
        'Admirals' : ':sea:',
        'Crushers' : ':seo:',
        'Marauders' : ':syd:',
        'Beavers' : ':tor:'
    }
    return teams.get(teamName, ':smile:')

def getPickTime(draftHtml):
    pickElement =  draftHtml.find('td', string=re.compile("Pick due")).text
    return pickElement

def getOnClock(draftHtml):
    onClockElement =  draftHtml.find('td', string=re.compile("Pick due"))
    onClockText = onClockElement.text
    teamOnClockText = onClockElement.previous_sibling.text
    return teamOnClockText + " " + onClockText

def getOnClockTeam(draftHtml):
    onClockElement =  draftHtml.find('td', string=re.compile("Pick due"))
    teamOnClockText = onClockElement.previous_sibling.text.split("(")
    return teamOnClockText[0]

def getPreviousPick(draftHtml):
    previousParent = draftHtml.find('td', string=re.compile("Pick due")).parent.previous_sibling
    previousPick = previousParent.contents[0].text
    previousTeam = previousParent.contents[1].text
    previousTeamIcon = getTeamIcon(previousTeam.split("(")[0])
    previousPlayer = previousParent.contents[2].text
    return previousTeamIcon + " " + previousPick + " : " + previousTeam +  " : " + previousPlayer

def getTimeFromFile():
    readtimefile = open('time.txt', 'r+')
    darfttime = readtimefile.readlines()
    readtimefile.close()
    if not darfttime:
        return " "
    else:
        return darfttime[0]

def sendMessage(channel, message):
    sc = slackclient.SlackClient(SLACK_TOKEN)
    print (sc.api_call("chat.postMessage", channel=channel, text=message,
                       ae_user='false', username='gubadraftbot', icon_emoji=':baseball:'))

if __name__ == "__main__":
    WAIT_DELAY = 30
    test = True
    while True:
        print("trace: trying again")
        res = requests.get('http://www.thefibb.net/cgi-bin/ootpou.pl?page=draftPicks')
        res.raise_for_status()
        noStarchSoup = bs4.BeautifulSoup(res.text, 'html.parser')
        timeDraft = getPickTime(noStarchSoup);
        timeInfo = getTimeFromFile()
        timeFile = open('time.txt', 'r+')
        if timeInfo.strip() != timeDraft.strip():
            timeFile.write(timeDraft)
            timeFile.close()

            onClockResult = getOnClock(noStarchSoup)
            previousPickResult = getPreviousPick(noStarchSoup)

            teamOnClock = getOnClockTeam(noStarchSoup)

            print(onClockResult)
            print(previousPickResult)

            previousPickPayload = "LAST PICK :"  + previousPickResult
            onClockPayLoad = "ON CLOCK: " + getTeamIcon(teamOnClock) + onClockResult
            sendMessage("test-thegubabot", previousPickPayload)
            sendMessage("test-thegubabot", onClockPayLoad)
            sendMessage("general", previousPickPayload)
            sendMessage("general", onClockPayLoad)
        time.sleep(WAIT_DELAY)
        timeFile.close()
        test=False
