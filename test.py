from pymongo import MongoClient
import os
import schedule
import time
from datetime import datetime, timedelta
from pytz import timezone
import requests
from MatchData import Match

cluster = MongoClient(os.getenv('MONGO_LINK'))

db = cluster['footballBot']
collection = db['userBalance']
betsCollection = db['Bets']

link = "https://v3.football.api-sports.io/fixtures?id=868086"
apiKey = 'f64adcb9a21a52f073e5c24da0666d6f'


headers = {
    'x-apisports-key' : apiKey,
}


# year = datetime.now(tz = timezone("UTC")).year
# month = datetime.now(tz = timezone("UTC")).month
# day = datetime.now(tz = timezone("UTC")).day

# datetime(year = year, month = month, day = day, hour = "", minute = "")



def job():

    matchObject = Match()

    data = matchObject.getData()


    data = list(map(lambda x: (x['fixture']['date'][:-9][11:]).replace(":", ""), data))

    data.sort(reverse = True)

    return(data[0])


time = job()

print(time)

nowTime = datetime.now(tz = timezone("UTC"))

hour = int(time[:2])
minute = int(time[2:])
year = nowTime.year
month = nowTime.month
day = nowTime.day

print(hour, minute)    

print(datetime(year = year, month = month, day = day, hour = hour, minute = minute, tzinfo = timezone("UTC")))


# def redeemBet():


#     IST = timezone('Asia/Kolkata')
#     now = datetime.now(IST) - timedelta(days = 1)
#     date_format = '%Y-%m-%d'
#     formattedDate = now.strftime(date_format)

#     print(formattedDate)

#     allData = betsCollection.find({'date' : formattedDate})

#     for data in allData:

#         redeemedValue = data['redeemed']

#         if redeemedValue == False:



#             teams = data['teams']

#             matchID = str(data['_id'])

#             winningTeam = getMatchWin(matchID)



#             if winningTeam in list(teams.keys()):

#                 userData = data['teams'][winningTeam]['userBets']
#                 winningTeamTotal = data['teams'][winningTeam]['teamTotalAmount']
#                 totalAmount = data['totalAmount']
            

#                 for item in userData.items():
#                     userID = item[0]
#                     amountBetted = item[1]

#                     amountEarnt = round(((int(amountBetted) / int(winningTeamTotal)) * int(totalAmount)))


#                     updateBalance(userID, 'add', int(amountEarnt))

#                 betsCollection.update_one({'_id' : matchID}, {'$set' : {'redeemed' : True}})

#             else:
#                 pass

#         elif redeemedValue == True:
#             raise redeemError(f'Match during {formattedDate} has already been redeemed')



# schedule.every().day.at("00:00").do(job)


# while True:
#     schedule.run_pending()
#     time.sleep(1)