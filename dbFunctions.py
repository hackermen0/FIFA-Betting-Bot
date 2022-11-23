from pymongo import MongoClient
import requests
from pytz import timezone
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timedelta
import os


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#if amount eneterd is more than user balance this exception is raised

class lowFunds(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


#if an bet for a day has already been redeemed this is raised

class redeemError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

cluster = MongoClient(os.getenv('MONGO_LINK'))

db = cluster['footballBot']
collection = db['userBalance']
betsCollection = db['Bets']

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#creates a balance for a discord user with the defualt amount of 1000

def createBalance(userID : int, userName : str):
    post = {
        '_id' : userID,
        'name' : userName,
        'balance' : 5000,
        'bonus' : 5

    }

    collection.insert_one(post)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#checks if the discord user has a balance using the user's id

def checkUserExists(userID):
    check = collection.find_one({'_id' : userID})

    if check == None:
        return False

    else:
        return True

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#returns the balance of a discord user
#if user doesnt have a balanace, it will also create a balance for them

def getBalance(userID, userName, autoCreate : bool = True):
    userData = collection.find_one({'_id' : userID})


    if userData == None:
        if autoCreate:
            createBalance(userID, userName)
            newUserData = collection.find_one({'_id' : userID})
            return newUserData['balance']
    else:
       return userData['balance']

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#updates the balance of a discord user
#"add" method will add a integer to the existing amount
#"sub" method will subtract a integer from the existing amount
#"sub" method also checks if the amount entered is more than the balance if true it raises lowFunds error(line 16)

def updateBalance(userID, method, amount : int):
    userData = collection.find_one({'_id' : userID})

    balance = int(userData['balance'])

    if method == 'add':
        updatedBalance = balance + amount

    elif method == 'sub':
        if balance >= amount:
            updatedBalance = balance - amount
        else:
            raise lowFunds(f'{userID} has insufficient funds')

    collection.update_one(
        {'_id' : userID}, 
        {'$set' : {'balance' : int(updatedBalance)}})


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def bonusUpdate(userID, amount):

    userData = collection.find_one({"_id" : userID})

    bonus = int(userData['bonus'])

    if bonus < 25:
        bonus += 1

    baseAmount = amount

    bonusAmount = round(((bonus / 100) * baseAmount))

    amountToGive = bonusAmount

    updateBalance(userID = userID, method = "add", amount = amountToGive)
    collection.update_one(
        {"_id" : userID},
        {"$set" : {"bonus" : bonus}}
    )

    return amountToGive




#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Checks if a discord user has already betted for a certain day
#If true it returns false
#Incase of a type error(when the first person is betting no bet is created so this makes sure the first person can bet) it returns False
#4/11/22 - Changed userID input to int instead of str as discord ID's are integers it's being changed to str later in the code 

def checkBetExists(matchID, userID : int):
    data = betsCollection.find_one({'_id' : matchID})

    try:

        if str(userID) in data['betList']:
            return True

        else:
            return False

    except TypeError:
        return False


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#It tries creating a bet first but if the bet already exists it updates it
#Increments the totalAmount and teamTotalAmount and adds the user's bet to the team they betted on
#Adds the user's id in betList so checkBetExists(line 104) can work
#4/11/22 - Changed userID input to int instead of str as discord ID's are integers it's being changed to str later in the code 

def updateBet(matchID, userID : int, team, amount : int):

    userID = str(userID)

    IST = timezone('UTC')
    now = datetime.now(IST) 
    date_format = '%Y-%m-%d'
    formattedDate = now.strftime(date_format)

    try:
        post = {
            '_id' : matchID,
            'totalAmount' : amount,
            'date' : formattedDate,
            'redeemed' : False,
            'betList' : [userID],
            'teams' : {
                team : {
                    'teamTotalAmount' : amount,
                    'userBets' : {
                        userID : amount
                    }
                }
            }
        }

        betsCollection.insert_one(post)

    
    except DuplicateKeyError:
        

        betsData = betsCollection.find_one({'_id' : matchID})
  

        betsCollection.update_one({'_id' : matchID}, {'$push' : {'betList' : userID}})
        totalAmount = betsData['totalAmount']
        newTotalAmount = totalAmount + amount

        teamsList = list(betsData['teams'].keys())

    
        if team in teamsList:

            teamTotalAmount = betsData['teams'][team]['teamTotalAmount']
            newTeamTotalAmount = teamTotalAmount + amount


            betsCollection.update_one({'_id' : matchID}, {'$set' : {f'teams.{team}.userBets.{userID}' : amount}})
            betsCollection.update_one({'_id' : matchID}, {'$set' : {'totalAmount' : newTotalAmount}})
            betsCollection.update_one({'_id' : matchID}, {'$set' : {f'teams.{team}.teamTotalAmount' : newTeamTotalAmount}})
            

        elif team not in teamsList:
            
            updatePost = {
                team : {
                    'teamTotalAmount' : amount,
                    'userBets' : {
                        userID : amount
                    }
                }
            }


            betsData['teams'].update(updatePost)


            betsCollection.update_one({'_id' : matchID}, {'$set' : {'teams' : betsData['teams']}})
            betsCollection.update_one({'_id' : matchID}, {'$set' : {'totalAmount' : newTotalAmount}})



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getMatchWin(matchID):

    link = f"https://v3.football.api-sports.io/fixtures?id={matchID}"

    headers = {
        'x-apisports-key' : "f64adcb9a21a52f073e5c24da0666d6f"
    }


    r = requests.get(link, headers = headers)


    data = r.json()

    homeTeam = data['response'][0]['teams']['home']
    awayTeam = data['response'][0]['teams']['away']

    if homeTeam['winner'] == "True":
        return homeTeam['name']

    elif awayTeam['winner'] == "True": 
        return awayTeam['name']

    else:
        return "None", (homeTeam['name'], awayTeam["name"])

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Gives the updatedBalance to all the users who betted on the winning team
#Updates the amount from the bets from the previous day(UTC)
#Gets match win data from the function getMatchWin(imported in line 6) using the match id 
#Formula to determine the amount of money to be incremented = (user's bet ammount / teamTotalAmount) * TotalAmount in the betting pool
#uses the updateBalance(line 82) to update the user's balance
#If there are 2 matches for one day it iterates over both matches and awards the winning user's
#If no one bets for the winning team it just passes

def redeemBet():


    UTC = timezone('UTC')
    now = datetime.now(UTC) - timedelta(days = 1)
    date_format = '%Y-%m-%d'
    formattedDate = now.strftime(date_format)

    print(formattedDate)

    allData = betsCollection.find({'date' : formattedDate})

    
    for data in allData:

        redeemedValue = data['redeemed']


        if redeemedValue == False:


            teams = data['teams']

            matchID = str(data['_id'])

            winningTeam = getMatchWin(matchID)

            print(type(winningTeam))

            if isinstance(winningTeam, tuple):

                    homeTeamName = winningTeam[1][0]
                    print(homeTeamName)
                    awayTeamName = winningTeam[1][1]


                    if homeTeamName in list(teams.keys()):

                        homeTeamData = data['teams'][homeTeamName]['userBets']

                        for item in homeTeamData.items():
                            userID = item[0]
                            amountBetted = item[1]

                            updateBalance(int(userID), 'add', int(amountBetted))  

                    if awayTeamName in list(teams.keys()):

                        awayTeamData = data['teams'][awayTeamName]['userBets']

                        for item in awayTeamData.items():
                            userID = item[0]
                            amountBetted = item[1]

                            updateBalance(int(userID), 'add', int(amountBetted))  


                    betsCollection.update_one({'_id' : matchID}, {'$set' : {'redeemed' : True}})

            else:

                if winningTeam in list(teams.keys()):

                    userData = data['teams'][winningTeam]['userBets']
                    winningTeamTotal = data['teams'][winningTeam]['teamTotalAmount']
                    totalAmount = data['totalAmount']
                

                    for item in userData.items():
                        userID = item[0]
                        amountBetted = item[1]

                        amountEarnt = round(((int(amountBetted) / int(winningTeamTotal)) * int(totalAmount)))
    

                        updateBalance(int(userID), 'add', int(amountEarnt))   
                              

                    betsCollection.update_one({'_id' : matchID}, {'$set' : {'redeemed' : True}})

        elif redeemedValue == True:
            raise redeemError(f'Match during {formattedDate} has already been redeemed')


            

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def getLeaderboard():

    def sort(e):
        return e[1]


    allList = list(collection.find())


    moneyList = list(map(lambda x: (x['_id'], x['balance']), allList))

    moneyList.sort(key = sort, reverse = True)

    return moneyList


def getStats():

        now = datetime.now()

        formattedData = now.strftime('%Y-%m-%d')

        data = betsCollection.find(({'date' : formattedData}))

        matchDataList = []

        for match in data:
            
            teams = list(match['teams'].keys())


            if len(teams) == 2:

                team1 = teams[0]
                team2 = teams[1]


                team1TotalAmount = match['teams'][team1]['teamTotalAmount']
                team2TotalAmount = match['teams'][team2]['teamTotalAmount']

                team1NumberOfBets = len(match['teams'][team1]['userBets'])
                team2NumberOfBets = len(match['teams'][team2]['userBets'])


                matchData = {
                    team1 : {
                        "totalAmount" : team1TotalAmount,
                        "numberOfBets" : team1NumberOfBets
                    },
                    team2 : {
                        "totalAmount" : team2TotalAmount,
                        'numberOfBets' : team2NumberOfBets
                    },
                    "numberOfTeams" : 2,
                }

                matchDataList.append(matchData)

            if len(teams) == 1:

                team1 = teams[0]

                team1TotalAmount = match['teams'][team1]['teamTotalAmount']
                team1NumberOfBets = len(match['teams'][team1]['userBets'])

                matchData = {
                     team1 : {
                        "totalAmount" : team1TotalAmount,
                        "numberOfBets" : team1NumberOfBets
                    },
                    "numberOfTeams" : 1,
                }

                matchDataList.append(matchData)


        return matchDataList

