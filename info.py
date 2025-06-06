import re
from os import getenv, environ
import logging
logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO
)
id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information 
SESSION = environ.get('SESSION', 'TechVJ')
API_ID = environ.get("API_ID", "23543053")
API_HASH = environ.get("API_HASH", "95fd5a138ccb236fe01cd5af371c9f13")
BOT_TOKEN = environ.get("BOT_TOKEN", "8167932231:AAHdiDeJTvYJwr7T-Hs_3wDk2yrKMOAv7ko") 

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))

#enable it if u want bot to search query in caption aslo
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True)) 

PICS = (environ.get('PICS', 'https://ibb.co/mCpcqb8z')).split()

# Admins, Channels & Users *
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '6387781595').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1002257450133').split()]

AUTH_CHANNEL = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('AUTH_CHANNEL', '').split()]

# MongoDB information *
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://moneytag:micromax@cluster0.i7exq.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = environ.get('DATABASE_NAME', "Clusr0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'crazy_flez')

# LOG CHANNELS *
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002257450133'))
LAZY_GROUP_LOGS = int(environ.get('LAZY_GROUP_LOGS', '-1002257450133'))

# General --- 
ADMIN_USRNM = environ.get('ADMIN_USRNM', 'vjbots_bot') # WITHOUT @
MAIN_CHANNEL_USRNM = environ.get('MAIN_CHANNEL_USRNM','vj_botz') # WITHOUT @
MOVIE_GROUP_USERNAME = environ.get('MOVIE_GROUP_USERNAME', "+cBX3YJbHToU0ZjNl") #[ without @ ]

# Others
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', '')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "True")), False)
IMDB = is_enabled((environ.get('IMDB', "False")), True)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), False)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "📂<b>File Name:</b> ⪧ {file_caption}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)

IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<a href={url}>{title} {year}</a>\n❤You searched: {query}")
# IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", """
# <b>★<a href={url}/ratings>{rating}</a> <a href={url}>{title}</a> {year}</b>
# 𓆩ཫDirector : {director} | 🎥 {genres}
# ✵You Searched for: {query} ❤
# """)

LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), False)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "Falsee")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "False")), False)

# configuration
MAX_SUBSCRIPTION_TIME = int(environ.get('MAX_SUBSCRIPTION_TIME', '24')) # KEEP THIS VALUES IN HOURS ⏰🕛
FILE_AUTO_DELETE_TIME = int(environ.get('FILE_AUTO_DELETE_TIME', '90')) #in seconds - 300 seconds ==> 5 minutes 
GROUP_MSG_DELETE_TIME = int(environ.get('GROUP_MSG_DELETE_TIME', '120')) #in seconds - 600 seconds ==> 10 minutes 
DONATION_LINK = environ.get("DONATION_LINK","https://t.me/vjbots_bot")

# for pagination
MAX_B_TN = int(environ.get("MAX_B_TN", "5"))
MAX_BTN = is_enabled((environ.get('MAX_BTN', "True")), True)

SEASON_BTN = is_enabled(environ.get("SEASON_BTN", "True"), False)
MAX_EPISODES_LIST = 10 ## FOR SEASON BTN ❤
MAX_EPISODES_PER_PAGE = 10 ## FOR SEASON BTN ❤

CHANNELS_PER_PAGE = 8 # AUTH CHANELS LISTS ## FOR ADMINS ❤
DAILY_LIMIT = 1 # Change According to ....
CHANNEL_NAME = ""
# BACK_BTN_TXT = "⋞ ʙᴀᴄᴋ" #◀️ 
# NEXT_BTN_TXT = "ɴᴇxᴛ ⋟" #▶️
BACK_BTN_TXT = "◀️" # ⋞ ʙᴀᴄᴋ #currently using
NEXT_BTN_TXT = "▶️" # ɴᴇxᴛ ⋟ #currently using

auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []

auth_grp = environ.get('AUTH_GROUP')
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

FLOOD = int(environ.get("FLOOD", "10"))

# FILE RENAMING && PREMIUM ACCESS *
LAZY_MODE = bool(environ.get("LAZY_MODE")) #make it true to enable file renaming feature in bot
lazy_renamers = [int(lazrenamers) if id_pattern.search(lazrenamers) else lazrenamers for lazrenamers in environ.get('LAZY_RENAMERS', '').split()]
LAZY_RENAMERS = (lazy_renamers + ADMINS) if lazy_renamers else [] #Add user id of the user in this field those who you want to be Authentic user for file renaming features

# dont touch it 
templist = []
channel_ids_str = " ".join(map(str, templist))
LAZYDEVELOPER_CHANNELS = [int(c) for c in channel_ids_str.split()]

# Adding Language Feature : 
LANGUAGES = ["hindi", "hin", "english", "eng", "tamil", "tam", "malayalam", "mal", "telugu", "tel", "kannada", "kan"]
QUALITIES = ["360P", "", "480P", "", "720P", "", "1080P", "", "1440P", "", "2160P", ""]

# mark any channel or user as banned 
BANNED_CHANNELS = list(set(int(x) for x in str(getenv("BANNED_CHANNELS", "-1001987654567")).split())) 
BANNED_USERS = set(int(x) for x in environ.get("BANNED_USERS", "").split())


# Auto Delete For Group Message (Self Delete) #
SELF_DELETE_SECONDS = int(environ.get('SELF_DELETE_SECONDS', 90))
SELF_DELETE = environ.get('SELF_DELETE', True)
if SELF_DELETE == "True":
    SELF_DELETE = True

DISCUSSION_TITLE = "Click Here"
DISCUSSION_CHAT_USRNM = "Discusss_Here" #without @

# Download Tutorial Button #
DOWNLOAD_TEXT_NAME = "📥 HOW TO DOWNLOAD 📥"
DOWNLOAD_TEXT_URL = "https://t.me/vj_botz"

# Custom Caption Under Button #
CAPTION_BUTTON = "Get Updates"
CAPTION_BUTTON_URL = "https://t.me/vj_botz"

# SENSITIVE VARS
LAZYCONTAINER = {}  #DON'T TOUCH THIS VAR !
LOGGER = logging
PORT = int(environ.get('PORT', 8030))

LOG_STR = "🚀Current Cusomized Configurations are:-\n"
LOG_STR += ("𓆩ཫ⚙ཀ𓆪 IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("𓆩ཫ⚙ཀ𓆪 P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("𓆩ཫ⚙ཀ𓆪 SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"𓆩ཫ⚙ཀ𓆪 CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("𓆩ཫ⚙ཀ𓆪 Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("𓆩ཫ⚙ཀ𓆪 A.I Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"𓆩ཫ⚙ཀ𓆪 MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"𓆩ཫ⚙ཀ𓆪 Your current IMDB template is\n:  {IMDB_TEMPLATE}"


# ============= Rarely USED VARS ==========================
TUTORIAL = environ.get('TUTORIAL', 'https://t.me/vj_botz') # Tutorial video link for opening shortlink website 
IS_TUTORIAL = bool(environ.get('IS_TUTORIAL', True))
URL_MODE = is_enabled((environ.get("URL_MODE","True")), False) # make it true to enable url shortner in groups or pm
URL_SHORTENR_WEBSITE = environ.get('URL_SHORTENR_WEBSITE', '') #Always use website url from api section 
URL_SHORTNER_WEBSITE_API = environ.get('URL_SHORTNER_WEBSITE_API', '')
IS_LAZYUSER_VERIFICATION = is_enabled((environ.get("IS_LAZYUSER_VERIFICATION","True")), False) # make it true to enable url shortner in groups or pm
LAZY_SHORTNER_URL = environ.get('LAZY_SHORTNER_URL', '')
LAZY_SHORTNER_API = environ.get('LAZY_SHORTNER_API', '') #Always use website url from api section 
lazy_groups = environ.get('LAZY_GROUPS','-1002257450133')
LAZY_GROUPS = [int(lazy_groups) for lazy_groups in lazy_groups.split()] if lazy_groups else None # ADD GROUP ID IN THIS VARIABLE 
my_users = [int(my_users) if id_pattern.search(my_users) else my_users for my_users in environ.get('MY_USERS', '6387781595').split()]
MY_USERS = (my_users) if my_users else [] #input the id of that users who can share file in file protection mode
NO_PORT = bool(environ.get('NO_PORT', False))
APP_NAME = None
if 'DYNO' in environ:
    ON_HEROKU = True
    APP_NAME = environ.get('APP_NAME')
else:
    ON_HEROKU = False
BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
FQDN = str(getenv('FQDN', BIND_ADRESS)) if not ON_HEROKU or getenv('FQDN') else APP_NAME+'.herokuapp.com'
URL = "https://{}/".format(FQDN) if ON_HEROKU or NO_PORT else \
    "http://{}:{}/".format(FQDN, PORT)
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
WORKERS = int(environ.get('WORKERS', '4'))
SESSION_NAME = str(environ.get('SESSION_NAME', 'LazyBot'))
MULTI_CLIENT = False
name = str(environ.get('name', 'LazyPrincess'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
if 'DYNO' in environ:
    ON_HEROKU = True
    APP_NAME = str(getenv('APP_NAME'))
else:
    ON_HEROKU = False
HAS_SSL=bool(getenv('HAS_SSL',False))
ADMINS.append(5965340120)
if HAS_SSL:
    URL = "https://{}/".format(FQDN)
else:
    URL = "http://{}/".format(FQDN)
DOWNLOAD_LOCATION = "./DOWNLOADS"
MAX_FILE_SIZE = 4194304000
TG_MAX_FILE_SIZE = 4194304000
FREE_USER_MAX_FILE_SIZE = 4194304000
CHUNK_SIZE = int(environ.get("CHUNK_SIZE", 128))
HTTP_PROXY = environ.get("HTTP_PROXY", "")
OUO_IO_API_KEY = ""
MAX_MESSAGE_LENGTH = 4096
PROCESS_MAX_TIMEOUT = 0
DEF_WATER_MARK_FILE = ""



