import sys

path = sys.path[0].replace('\Modules', '')
sys.path.append(path)

from pymongo import MongoClient
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
        'balance' : 1000,

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

def getBalance(userID, userName):
    userData = collection.find_one({'_id' : userID})

    if userData == None:
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

    IST = timezone('Asia/Kolkata')
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
#Gives the updatedBalance to all the users who betted on the winning team
#Updates the amount from the bets from the previous day(IST)
#Gets match win data from the function getMatchWin(imported in line 6) using the match id 
#Formula to determine the amount of money to be incremented = (user's bet ammount / teamTotalAmount) * TotalAmount in the betting pool
#uses the updateBalance(line 82) to update the user's balance
#If there are 2 matches for one day it iterates over both matches and awards the winning user's
#If no one bets for the winning team it just passes

def redeemBet():


    IST = timezone('Asia/Kolkata')
    now = datetime.now(IST) - timedelta(days = 1)
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



            if winningTeam in list(teams.keys()):

                userData = data['teams'][winningTeam]['userBets']
                winningTeamTotal = data['teams'][winningTeam]['teamTotalAmount']
                totalAmount = data['totalAmount']
            

                for item in userData.items():
                    userID = item[0]
                    amountBetted = item[1]

                    amountEarnt = round(((int(amountBetted) / int(winningTeamTotal)) * int(totalAmount)))
  

                    updateBalance(userID, 'add', int(amountEarnt))

                betsCollection.update_one({'_id' : matchID}, {'$set' : {'redeemed' : True}})

            else:
                pass

        elif redeemedValue == True:
            raise redeemError(f'Match during {formattedDate} has already been redeemed')




       
