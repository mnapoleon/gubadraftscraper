import re, requests, bs4, slackclient, time, configparser

config = configparser.ConfigParser()
config.read('config.properties')

SLACK_TOKEN = config.get('Slack', 'SlackToken')

def get_team_icon(teamName):
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

def get_pick_time(draftHtml):
    pickElement =  draftHtml.find('td', string=re.compile("Pick due")).text
    return pickElement

def get_on_clock(draftHtml):
    onClockElement =  draftHtml.find('td', string=re.compile("Pick due"))
    onClockText = onClockElement.text
    teamOnClockText = onClockElement.previous_sibling.text
    return teamOnClockText + " " + onClockText

def get_on_clock_team(draftHtml):
    onClockElement =  draftHtml.find('td', string=re.compile("Pick due"))
    teamOnClockText = onClockElement.previous_sibling.text.split("(")
    return teamOnClockText[0]

def get_previous_pick(draftHtml):
    previousParent = draftHtml.find('td', string=re.compile("Pick due")).parent.previous_sibling
    previousPick = previousParent.contents[0].text
    previousTeam = previousParent.contents[1].text
    previousTeamIcon = get_team_icon(previousTeam.split("(")[0])
    previousPlayer = previousParent.contents[2].text
    return previousTeamIcon + " " + previousPick + " : " + previousTeam +  " : " + previousPlayer

def get_time_from_file():
    readtimefile = open('time.txt', 'r+')
    drafttime = readtimefile.readlines()
    readtimefile.close()
    if not drafttime:
        return " "
    else:
        return drafttime[0]

def set_last_pick_num(draftHtml):
    previousParent = draftHtml.find('td', string=re.compile("Pick due")).parent.previous_sibling
    picknum = previousParent.contents[0].text
    pickNumFile = open('picknum.txt', 'r+')
    pickNumFile.write(picknum)
    pickNumFile.close()

def send_message(channel, message):
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
        timeDraft = get_pick_time(noStarchSoup);
        timeInfo = get_time_from_file()
        set_last_pick_num(noStarchSoup)

        timeFile = open('time.txt', 'r+')
        if timeInfo.strip() != timeDraft.strip():
            timeFile.write(timeDraft)
            timeFile.close()

            onClockResult = get_on_clock(noStarchSoup)
            previousPickResult = get_previous_pick(noStarchSoup)

            teamOnClock = get_on_clock_team(noStarchSoup)

            print(onClockResult)
            print(previousPickResult)

            previousPickPayload = "LAST PICK :"  + previousPickResult
            onClockPayLoad = "ON CLOCK: " + get_team_icon(teamOnClock) + onClockResult
            send_message("test-thegubabot", previousPickPayload)
            send_message("test-thegubabot", onClockPayLoad)
            #send_message("general", previousPickPayload)
            #send_message("general", onClockPayLoad)
        time.sleep(WAIT_DELAY)
        timeFile.close()
        test=False
