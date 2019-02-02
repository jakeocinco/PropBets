from django.shortcuts import render

from http import cookies
import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

json_key = json.load(open('google-creds_2.json')) # json credentials you downloaded earlier

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('google-creds_2.json', scope) # get email and key from creds
#credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) # get email and key from creds

file = gspread.authorize(credentials) # authenticate with Google

sheet = file.open("sbb2017").sheet1 # open sheet


UserList = ["Jake","Jarod","Jack","Tom","Tyler","Zack","Josh"]

UserCols = {
    "Jake":2,
    "Jarod":3,
    "Jack":4,
    "Tom":5,
    "Tyler":6,
    "Zack":7,
    "Josh":8
}

Scores = {
    "Jake":0,
    "Jarod":0,
    "Jack":0,
    "Tom":0,
    "Tyler":0,
    "Zack":0,
    "Josh":0
}

newScores = {
    "Jake":0,
    "Jarod":0,
    "Jack":0,
    "Tom":0,
    "Tyler":0,
    "Zack":0,
    "Josh":0
}

logged_In = 'N'
current_user = ""
current_pass = ""

bets = []

nums = [2, 3, 4,5, 6, 7,8]
#for x in i:
    #info = sheet.col_values(x);

    #bets.append( {'name':info[0],'coin':info[3],
        #'commercial_1':info[4],
        #'commercial_2':info[5],
        #'firstScore':info[6]
#    })


def updateScoreTable(line):
    for user in Scores:
        if user in line:
            loc = line.find(user) + len(user) + 1
            num = int(line[loc:(loc+1)])
            newScores[user] += num;

def checkLocks(info):
    locks = ['','','','']
    index = 0
    for inf in info:
        if 'locked' in inf:
            if len(inf['locked']) > 2:
                if inf['locked'][2] == 'Y':
                    locks[index] = 'Y'
                index += 1
                if index >= 3:
                    break

    return locks

def getWinners(info):

    coin_flipWinner = ''
    commercial_1Winner = ''
    commercial_2Winner = ''
    scorerWinner = ''
    defensiveWinner = ''
    Q1Winner = ''
    Q2Winner = ''
    Q3Winner = ''
    Q4Winner = ''
    WinnerWinner = ''
    OverUnderWinner = ''
    gatoradeWinner = ''
    MVP_Winner = ''

    for name in UserList:
        newScores[name] = 0;


    for inf in info:
        if '' in inf:
            str = inf['']
            if 'Coin' in str:
                coin_flipWinner = inf['Winners']
                updateScoreTable(coin_flipWinner)
            elif 'First Commercial' in str:
                if 'option 1' in str:
                    commercial_1Winner = inf['Winners']
                    updateScoreTable(commercial_1Winner)
                elif 'option 2' in str:
                    commercial_2Winner = inf['Winners']
                    updateScoreTable(commercial_2Winner)
            elif 'touchdown (Player' in str:
                scorerWinner = inf['Winners']
                updateScoreTable(scorerWinner)
            elif 'Defensive touchdown' in str:
                defensiveWinner = inf['Winners']
                updateScoreTable(defensiveWinner)
            elif 'Q1' in str:
                Q1Winner = inf['Winners']
                updateScoreTable(Q1Winner)
            elif 'Q2' in str:
                Q2Winner = inf['Winners']
                updateScoreTable(Q2Winner)
            elif 'Q3' in str:
                Q3Winner = inf['Winners']
                updateScoreTable(Q3Winner)
            elif 'Q4' in str:
                Q4Winner = inf['Winners']
                updateScoreTable(Q4Winner)
            elif 'Winner' in str:
                WinnerWinner = inf['Winners']
                updateScoreTable(WinnerWinner)
            elif 'Over/Under' in str:
                OverUnderWinner = inf['Winners']
                updateScoreTable(OverUnderWinner)
            elif 'Gatorade' in str:
                gatoradeWinner = inf['Winners']
                updateScoreTable(gatoradeWinner)
            elif 'MVP' in str:
                MVP_Winner = inf['Winners']
                updateScoreTable(MVP_Winner)
            #else:
                #print(str)

    for user in Scores:
        if Scores[user] != newScores[user]:
            sheet.update_cell(3,UserCols[user],newScores[user])
            Scores[user] = newScores[user]

    return [coin_flipWinner, commercial_1Winner, commercial_2Winner, scorerWinner,defensiveWinner,Q1Winner,Q2Winner,Q3Winner,Q4Winner,WinnerWinner,OverUnderWinner,gatoradeWinner,MVP_Winner]

def setScoreBoard(info):

    list_keys = sorted(Scores, key=Scores.get, reverse=True)
    list_values = sorted(Scores.values(), reverse=True)

    megaArray = []

    index = 0
    for r in list_keys:
        megaArray += [[r, list_values[index]]]

        index = index + 1

    return megaArray

def home(request):

    # TODO - make score pop ups over each cell
    # TODO - put all of this into methods and arrays, too much repition (html too)
    # TODO - refactor methods to not take whole dict (create more calls to each method, while breaking apart work)

    info = sheet.get_all_records();

    global logged_In
    global current_user
    global current_pass
    global coin_flip
    global commercial_1
    global commercial_2
    global firstTD
    global defensiveScorer
    global scoreQ1
    global scoreQ2
    global scoreQ3
    global scoreQ4
    global winner
    global overUnder
    global gatorade
    global MVP
    global won
    global winArray

    response = ''
    bets = []


    winArray = getWinners(info)
    leaderBoard = setScoreBoard(info)
    locks = checkLocks(info)



    s = request.POST.get('user')
    if s is not None:
        current_user = s

    current_pass = request.POST.get('pass')


    s = request.POST.get('coin_flip')
    if s is not None:
        coin_flip = s
        print(coin_flip)

    s = request.POST.get('commercial_1')
    if s is not None:
        commercial_1 = s
        print(commercial_1)

    s = request.POST.get('commercial_2')
    if s is not None:
        commercial_2 = s
        print(commercial_2)

    s = request.POST.get('firstTD')
    if s is not None:
        firstTD = s
        print(firstTD)

    s = request.POST.get('defensiveScorer')
    if s is not None:
        defensiveScorer = s
        print(defensiveScorer)

    s = request.POST.get('scoreQ1')
    if s is not None:
        scoreQ1 = s
        print(scoreQ1)

    s = request.POST.get('scoreQ2')
    if s is not None:
        scoreQ2 = s
        print(scoreQ2)

    s = request.POST.get('scoreQ3')
    if s is not None:
        scoreQ3 = s
        print(scoreQ3)

    s = request.POST.get('scoreQ4')
    if s is not None:
        scoreQ4 = s
        print(scoreQ4)

    s = request.POST.get('winner')
    if s is not None:
        winner = s
        print(winner)

    s = request.POST.get('overUnder')
    if s is not None:
        overUnder = s
        print(overUnder)

    s = request.POST.get('gatorade')
    if s is not None:
        gatorade = s
        print(gatorade)

    s = request.POST.get('MVP')
    if s is not None:
        MVP = s
        print(MVP)

    s = request.POST.get('responceType')
    if s is not None:
        response = s
        print(response)


    # TODO - pass information using post that says wether or not the user is logging in or creating responces
    if 'r' in response:
        print(response + " 2")
        if logged_In == "Y":
            print('logging in')

            # TODO - make it so it only updates new values?
            # if it equals value in 'info' do not update - this may be important when people are using it
            sheet.update_cell(4,UserCols[current_user],coin_flip)
            sheet.update_cell(5,UserCols[current_user],commercial_1)
            sheet.update_cell(6,UserCols[current_user],commercial_2)
            sheet.update_cell(7,UserCols[current_user],firstTD)
            sheet.update_cell(8,UserCols[current_user],defensiveScorer)
            sheet.update_cell(9,UserCols[current_user],scoreQ1)
            sheet.update_cell(10,UserCols[current_user],scoreQ2)
            sheet.update_cell(11,UserCols[current_user],scoreQ3)
            sheet.update_cell(12,UserCols[current_user],scoreQ4)
            sheet.update_cell(13,UserCols[current_user],winner)
            sheet.update_cell(14,UserCols[current_user],overUnder)
            sheet.update_cell(15,UserCols[current_user],gatorade)
            sheet.update_cell(16,UserCols[current_user],MVP)

            context = {
                'bets'  : bets,
                'current_user': current_user,
                'current_pass':current_pass,
                'coin_flip' : coin_flip,
                'commercial_1':commercial_1,
                'commercial_2':commercial_2,
                'firstTD':firstTD,
                'defensiveScorer':defensiveScorer,
                'scoreQ1':scoreQ1,
                'scoreQ2':scoreQ2,
                'scoreQ3':scoreQ3,
                'scoreQ4':scoreQ4,
                'winner':winner,
                'overUnder':overUnder,
                'gatorade':gatorade,
                'MVP':MVP,
                'Ranks':leaderBoard,
                'lock1':locks[0],
                'lock2':locks[1],
                'lock3':locks[2],
                'lock4':locks[3]
            }

        else:

            context = {
                'bets'  : bets,
                'current_user': '',
                'current_pass':'',
                'coin_flip' : 'coin_flip',
                'commercial_1':'commercial_1',
                'commercial_2':'commercial_2',
                'firstTD':'firstTD',
                'defensiveScorer':'defensiveScorer',
                'scoreQ1':'scoreQ1',
                'scoreQ2':'scoreQ2',
                'scoreQ3':'scoreQ3',
                'scoreQ4':'scoreQ4',
                'winner':'winner',
                'overUnder':'overUnder',
                'gatorade':'gatorade',
                'MVP':'MVP',
                'Ranks':leaderBoard,
                'lock1':locks[0],
                'lock2':locks[1],
                'lock3':locks[2],
                'lock4':locks[3]
            }
    elif response == 'lo':
        current_user = ''

        context = {
            'bets'  : bets,
            'current_user': '',
            'current_pass':'',
            'coin_flip' : 'coin_flip',
            'commercial_1':'commercial_1',
            'commercial_2':'commercial_2',
            'firstTD':'firstTD',
            'defensiveScorer':'defensiveScorer',
            'scoreQ1':'scoreQ1',
            'scoreQ2':'scoreQ2',
            'scoreQ3':'scoreQ3',
            'scoreQ4':'scoreQ4',
            'winner':'winner',
            'overUnder':'overUnder',
            'gatorade':'gatorade',
            'MVP':'MVP',
            'Ranks':leaderBoard,
            'lock1':locks[0],
            'lock2':locks[1],
            'lock3':locks[2],
            'lock4':locks[3]
        }
    elif response == 'login' or True:

        if current_user in UserList:
            if current_pass == sheet.cell(2, UserCols[current_user]).value: # # TODO:
                print(current_user)
                logged_In = 'Y'

                for inf in info:
                    if '' in inf:
                        str = inf['']

                        if 'Coin' in str:
                            coin_flip = inf[current_user]
                            print(coin_flip)
                        elif 'First Commercial' in str:
                            if 'option 1' in str:
                                commercial_1 = inf[current_user]
                            elif 'option 2' in str:
                                commercial_2 = inf[current_user]
                        elif 'touchdown (Player' in str:
                            firstTD = inf[current_user]
                        elif 'Defensive touchdown' in str:
                            defensiveScorer = inf[current_user]
                        elif 'Q1' in str:
                            scoreQ1 = inf[current_user]
                        elif 'Q2' in str:
                            scoreQ2 = inf[current_user]
                        elif 'Q3' in str:
                            scoreQ3 = inf[current_user]
                        elif 'Q4' in str:
                            scoreQ4 = inf[current_user]
                        elif 'Winner' in str:
                            winner = inf[current_user]
                        elif 'Over/Under' in str:
                            overUnder = inf[current_user]
                        elif 'Gatorade' in str:
                            gatorade = inf[current_user]
                        elif 'MVP' in str:
                            MVP = inf[current_user]
                        else:
                            print(str)


            context = {
                'bets'  : bets,
                'current_user': current_user,
                'current_pass':current_pass,
                'coin_flip' : coin_flip,
                'commercial_1':commercial_1,
                'commercial_2':commercial_2,
                'firstTD':firstTD,
                'defensiveScorer':defensiveScorer,
                'scoreQ1':scoreQ1,
                'scoreQ2':scoreQ2,
                'scoreQ3':scoreQ3,
                'scoreQ4':scoreQ4,
                'winner':winner,
                'overUnder':overUnder,
                'gatorade':gatorade,
                'MVP':MVP,
                'Ranks':leaderBoard,
                'lock1':locks[0],
                'lock2':locks[1],
                'lock3':locks[2],
                'lock4':locks[3]
            }
        else:
            context = {
                'bets'  : bets,
                'current_user': '',
                'current_pass':'',
                'coin_flip' : 'coin_flip',
                'commercial_1':'commercial_1',
                'commercial_2':'commercial_2',
                'firstTD':'firstTD',
                'defensiveScorer':'defensiveScorer',
                'scoreQ1':'scoreQ1',
                'scoreQ2':'scoreQ2',
                'scoreQ3':'scoreQ3',
                'scoreQ4':'scoreQ4',
                'winner':'winner',
                'overUnder':'overUnder',
                'gatorade':'gatorade',
                'MVP':'MVP',
                'Ranks':leaderBoard,
                'lock1':locks[0],
                'lock2':locks[1],
                'lock3':locks[2],
                'lock4':locks[3]
            }



    for x in nums:

        info = sheet.col_values(x);

        name = info[0]
        personalWinnersArray = ['','','','','','','','','','','','',''];

        index = 0
        for w in winArray:
            if name in w:
                #sets color of winners
                personalWinnersArray[index] = '#0ace00'

            index = index + 1

        bets.append( {
            'name':name,
            'coin':info[3],
            'commercial_1':info[4],
            'commercial_2':info[5],
            'firstScore':info[6],
            'defensiveTD':info[7],
            'Q1':info[8],
            'Q2':info[9],
            'Q3':info[10],
            'Q4':info[11],
            'winner':info[12],
            'OverUnder':info[13],
            'gatorade':info[14],
            'MVP':info[15],
            'coin_Color':personalWinnersArray[0],
            'commercial_1_Color':personalWinnersArray[1],
            'commercial_2_Color':personalWinnersArray[2],
            'firstScore_Color':personalWinnersArray[3],
            'defensiveTD_Color':personalWinnersArray[4],
            'Q1_Color':personalWinnersArray[5],
            'Q2_Color':personalWinnersArray[6],
            'Q3_Color':personalWinnersArray[7],
            'Q4_Color':personalWinnersArray[8],
            'winner_Color':personalWinnersArray[9],
            'OverUnder_Color':personalWinnersArray[10],
            'gatorade_Color':personalWinnersArray[11],
            'MVP_Color':personalWinnersArray[12]
        })

    return render(request, 'Meeting/home.html',context)



def about(request):
    return render(request, 'Meeting/about.html',{'title':'About'})
