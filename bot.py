import telebot
import requests
import random
import google.oauth2.credentials
#import google_auth_oauthlib.flow
import googleapiclient.discovery
from PIL import Image
from urllib3.util import parse_url
from io import BytesIO


# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/customsearch/']
API_SERVICE_NAME = "customsearch"
API_VERSION = 'v1'

token = "591889511:AAEPnd_qaD_q5VpCLYptRnbOhAdnMm8CCU8" 
API_KEY = "AIzaSyAWnU2keQYIZZdhU77dTRcRDZfsxsmNxsM"
EngineID = "003285803633102658846:cddtcxueg00"
bot = telebot.TeleBot(token)
HELP_MSG = "This is Photo Bot. Ask me for photos using command /photo"
link = "https://www.google.co.in/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
	print(message)
	bot.reply_to(message, HELP_MSG)

@bot.message_handler(commands=['hello'])
def handle_emoji(message):
	print(message)
	bot.reply_to(message, "This was an emoji")

@bot.message_handler(commands=['photo'])
def response(message):
	print(message)
	res = service.cse().list(
      q=message.text,
      cx=EngineID,
      imgType="photo",
      num=10,
    ).execute()
	n=len(res['items'])
	i=random.randint(1,(n-1))

	global link
	
	link = res['items'][i]['pagemap']['cse_image'][0]['src']
	link=parse_url(link)
	link=link.scheme+'://'+link.host+link.path

	f = open('sample.jpeg','wb')
	f.write(requests.get(link).content)
	f.close()

	bio = BytesIO()
	bio.name = 'sample.jpeg'
	image = Image.open('sample.jpeg')
	image.save(bio, 'JPEG')
	bio.seek(0)
	bot.send_photo(message.chat.id, photo=bio)

@bot.message_handler(func=lambda message: True)
def echo(message):
	print(message)
	bot.reply_to(message,message.text)

if __name__=="__main__":
	service = googleapiclient.discovery.build(
		API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)
	
	bot.polling(none_stop=False, interval=0, timeout=200)
	