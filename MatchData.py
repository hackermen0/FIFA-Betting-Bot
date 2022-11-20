import os
import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import date



class Match():

    def __init__(self):


        #date format = str(YYYY-MM-DD)
        self.dateToday = date.today()

        apiKey = 'f64adcb9a21a52f073e5c24da0666d6f'
        baseLink = 'https://v3.football.api-sports.io'

        leaugeID = '1'
        season = '2022'

        # statusLink = f'{baseLink}/status'
        fixturesLink = f'{baseLink}/fixtures?league={leaugeID}&season={season}'

        headers = {
            'x-apisports-key' : apiKey,
        }

        r = requests.get(fixturesLink, headers = headers)

        self.data = r.json()


    def getData(self) -> list:


        matchesToday = []

        #date format = str(YYYY-MM-DD)   

        for fixture in self.data['response']:
            if fixture['fixture']['date'][:-15] == str(self.dateToday):
                matchesToday.append(fixture)

        return matchesToday

    def createBanner(self, pos):

        data = self.getData()


     
        homeTeamLogo = data[pos]['teams']['home']['logo']
        awayTeamLogo = data[pos]['teams']['away']['logo']

        matchweek = data[pos]['league']['round']

        with open("./static/images/homeTeam.png", 'wb') as f:
            
            r = requests.get(homeTeamLogo)
            f.write(r.content)


        with open("./static/images/awayTeam.png", 'wb') as f:
            
            r = requests.get(awayTeamLogo)
            f.write(r.content)

        
        homeTeam = Image.open('./static/images/homeTeam.png').convert("RGBA")
        awayTeam = Image.open('./static/images/awayTeam.png').convert("RGBA")

        resizedHomeTeam = homeTeam.resize((225, 125))
        resizedAwayTeam = awayTeam.resize((225, 125))

        background = Image.new("RGBA", (827, 434), (232, 238, 239))

        backgroundDraw = ImageDraw.Draw(background)

        robotoSemiBold = ImageFont.truetype("./static/fonts/Roboto-Medium.ttf", 31)
        robotoExtraBold = ImageFont.truetype("./static/fonts/Roboto-Bold.ttf", 42)

        backgroundDraw.text((293,90), matchweek, fill=(0,0,0), font = robotoSemiBold)
        backgroundDraw.text((388,242), "VS", fill=(0,0,0), font = robotoExtraBold)

        print(resizedHomeTeam.size[0])
        print(resizedAwayTeam.size[0])

        homeTeamXcoordinate = round((388 - resizedHomeTeam.size[0]) / 2)
        awayTeamXcoordinate = 430 + round((388 - resizedAwayTeam.size[0]) / 2)

        background.paste(resizedHomeTeam, (homeTeamXcoordinate, 195), resizedHomeTeam)
        background.paste(resizedAwayTeam, (awayTeamXcoordinate, 195), resizedAwayTeam)

        background.save(f"./static/images/matchBanner{pos}.png")
        os.remove("./static/images/homeTeam.png")
        os.remove("./static/images/awayTeam.png")



        

