"""
@author Mr Suman Biswas
@github https://github.com/mrsumanbiswas
@Telegram_Bot  MrDizzy_bot
"""
############  IMPORTS  ##########
import os
import re
import json
import gtts
import random
import pymongo
import telebot
import requests
import wikipedia
import googlesearch
from time import strftime
from bs4 import BeautifulSoup

############  CODE  #############
Type = 'cancel'
BOT_API = os.environ["BOT_API"]
MONGODB = os.environ["MONGODB"]
# DATABASE CONNECTION #####
"""

"""

# MONGODB CONNECTION


def dbConnect():
    client = pymongo.MongoClient(host=MONGODB)

    db = client['teleBot']
    user = db['userDB']
    history = db['chatDB']

    collection = {
        "user": user,
        "history": history
    }
    return collection

# CLIENT DETAILS


def clientDetails(collection, time, chat_id, fullName, userName):
    userExists = False
    document = {
        "time": time,
        "chat_id": chat_id,
        "fullName": fullName,
        "userName": userName
    }
    for x in collection.find({"userName": userName}):
        userExists = True
    if not userExists:
        collection.insert_one(document)

# CHAT HISTOY


def chatHistory(collection, time, chat_id, fullName, message):
    doucment = {
        "time": time,
        "chat_id": chat_id,
        "fullName": fullName,
        "message": message
    }
    collection.insert_one(doucment)


# MODULE #####
"""

"""

# SEARCH ENGINE


def gSearch(quary: str):
    data = "No reasult found ..."
    try:
        data = googlesearch.search(term=quary, num_results=20)
    except Exception as e:
        data = data + "\nError : " + e
    return data

# IMAGE SCAPER


def imgScraping(quary):
    """

    """
    ImgLink = []
    u_agnt = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
    }

    search_url = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q=' + quary
    response = requests.get(search_url, headers=u_agnt)
    html = response.text
    b_soup = BeautifulSoup(html, 'html.parser')
    results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})
    count = 0
    for res in results:
        try:
            link = res['data-src']
            ImgLink.append(link)
            count = count + 1
            if (count >= 15):
                break
        except KeyError:
            continue
    if ImgLink != []:
        return ImgLink

# VACCINE SLOAT


def Vaccine(pincode):
    date = str(int(strftime('%d'))+1) + str(strftime('-%m-%Y'))
    try:
        data = f"No Slot available for {date} in {pincode}"
        api_request = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={date}" + \
            "accept: application/json" + "Accept-Language: en_US"
        response: list = json.loads(
            requests.get(url=api_request).text
        )['sessions']
        if response != []:
            for i in range(len(response)):
                for key in response[i]:
                    value = response[i][f'{key}']
                    data += f"{key.replace('_',' ')} -> {value}\n\n"
        return data

    except Exception as e:
        return "Error : " + str(e)

# WIKIPEDIA


def Wikipedia(quary: str) -> str:
    try:
        quary: str = quary.replace("summary:", "")
        Summary = wikipedia.summary(quary, sentences=10)
        texts2 = re.sub("\[.*?\]", "", Summary)
        texts3 = re.sub("\(.*?\)", "", texts2)
        Summary = texts3.replace(")", "").replace("(", "").replace("=", "")
        return Summary
    except:
        return f"Sorry nothing match about : {quary}"


# LOGIC


class main_handler():
    def __init__(self, bot, message) -> None:
        """
        """
        self.bot = bot
        self.message = message
        msg = message.text.lower()

        if Type == 'cancel':
            self.text(
                "This is a eco of your message ::\n"+message.text
            )
            self.audio(
                self.tts(msg)
            )
            self.text(
                """\
/find --> search over internet
/about --> gives info in audio format
/pic --> gives photos form web
/vaccine --> gives Indian vaccination slot info
/details --> gives your telegram info
/dizzy --> gives info about the bot
                """
            )

        elif Type == 'find':
            for x in gSearch(msg):
                self.text(x)

        elif Type == 'about':
            txt = Wikipedia(msg)
            self.text(txt)
            self.audio(
                path=self.tts(txt)
            )

        elif Type == 'pic':
            for pic in imgScraping(msg):
                self.image(pic)

        elif Type == 'vaccine':
            if len(msg) == 6:
                self.text(Vaccine(msg))
            else:
                self.text("Please provide a valid Indian pincode")

    def text(self, text: str):
        self.bot.send_message(
            chat_id=self.message.chat.id,
            text=text
        )

    def audio(self, path: str):
        self.bot.send_audio(
            chat_id=self.message.chat.id,
            audio=open(f'{path}', 'rb'))
        os.system(f'rm -r {path}')

    def image(self, path: str):
        self.bot.send_photo(
            self.message.chat.id,
            photo=path
        )

    def tts(self, text: str):
        fileName = random.randint(a=1, b=10)
        fileName = str(fileName) + ".mp3"
        try:
            gtts.gTTS(
                text=text
            ).save(
                savefile=fileName
            )
            return fileName
        except Exception as e:
            text("Error : " + e)


# EXECUTION

def main():
    bot = telebot.TeleBot(token=BOT_API)

    @bot.message_handler(commands=['start'])
    def commands(message):
        chat_id = message.chat.id
        fullName = f'{message.from_user.first_name} ' + \
            f'{message.from_user.last_name}'
        userName = message.from_user.username

        clientDetails(
            collection=dbConnect()['user'],
            time=strftime('%H:%M:%S || %d.%m.%Y || %z'),
            chat_id=chat_id,
            fullName=fullName,
            userName=userName
        )
        bot.send_message(
            chat_id,
            text=f"Welcome {fullName}.\nI'm Mr Dizzy here for you."
        )

    @bot.message_handler(commands=['details'])
    def commands(message):
        bot.send_message(
            message.chat.id,
            text=f"""\
First Name : {message.from_user.first_name}
Last Name : {message.from_user.last_name}
User Name : @{message.from_user.username}"""
        )

    @bot.message_handler(commands=['dizzy'])
    def commands(message):
        bot.send_message(
            message.chat.id,
            text="Not now I shall tell you letter...\nI'm a bot..."
        )

    @bot.message_handler(commands=['find', 'about', 'pic', 'vaccine', 'cancel'])
    def commands(message):
        global Type
        Type = message.text.replace('/', '')
        replys = {
            'find': 'What do you want to find ? \nI shall bring that to you.',
            'about': 'What information do you want?\nI shall give you a mp3 file with that.',
            'pic': 'Let me know what picture you want.\nI shall try my best.',
            'vaccine': "Please provide me the zipcode/pincode (Indian).\nI shall show you slots available for next day.",
            'cancel': 'Alright!',
        }

        text = replys[Type]
        if Type != "cancel":
            text += '\nIf noting then send /cancel'

        bot.send_message(
            message.chat.id,
            text=text
        )

    @bot.message_handler()
    def handler(message):
        global Type
        chat_id = message.chat.id
        fullName = f'{message.from_user.first_name} ' + \
            f'{message.from_user.last_name}'
        Message = message.text

        chatHistory(
            collection=dbConnect()['history'],
            time=strftime('%H:%M:%S || %d.%m.%Y || %z'),
            chat_id=chat_id,
            fullName=fullName,
            message=Message
        )

        try:
            main_handler(bot, message)
            Type = "cancel"
        except Exception as e:
            bot.reply_to(message, "err: " + str(e))
    bot.polling(non_stop=True, skip_pending=True)


########### Runner ##############
if __name__ == "__main__":
    try:
        print("Bot is up and running!")
        try:
            main()
        except:
            main()
    except:
        try:
            main()
        except:
            main()
        print("Bot got some error!")