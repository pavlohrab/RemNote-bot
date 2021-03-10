# Import some libraries
import logging
from bs4 import BeautifulSoup 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import *
import os, json, requests, re
from datetime import datetime as dt
import datetime
from sqlalchemy import create_engine
import pandas as pd
import psycopg2


# USER defined variables
TOKEN = ''
REMNOT_API= ''
USER_ID = ''
HEROKU_NAME = 'https://limitless-peak-12878.herokuapp.com/'
HOME_DIR = 'Saved Telegram'

# Some global variables
PORT = int(os.environ.get('PORT', 5000))
NOTE_ID = None
PARENT = None
NOTE = None
MEDIA_ID = None
FIRST, SECOND, THIRD, FOURTH = range(4)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Get the todays date!
def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

today = custom_strftime('%B {S}, %Y', dt.now())

################### Send Notes #############################
def send_note(text, parent=None, link=False, doc=None):
    global REMNOT_API, USER_ID, DOCUMENT, MEDIA_ID, today, URL
    url_post="https://api.remnote.io/api/v0/create"
    parent_Id = parent
    if parent == None:
        parent_Id = get_daily_rem()
    if parent_Id == None:
        parent_Id = search_parent()
        text = text + "#[["+today+"]]"
    par={
    "apiKey": REMNOT_API,
    "userId":USER_ID,
    "text": text,
    "parentId": parent_Id
    }
    if link == True:
        par['isDocument'] = True
        par['source'] = URL
        reqs = requests.get(URL) 
        soup = BeautifulSoup(reqs.text, 'html.parser') 
        try:
            par['text'] =  str(soup.find_all('title')[0].get_text()) + '#[['+today+']]'
        except:
            par['text'] = str(URL)
    elif DOCUMENT==True:
        par['source'] = open(f"{MEDIA_ID}.pdf", 'rb')
        par['isDocument'] = True
        par['text'] = MEDIA_ID
    created_rem = requests.post(url_post, data=par)
    return created_rem.json()['remId']

def get_daily_rem():
    global REMNOT_API, USER_ID
    url_get_by_name = "https://api.remnote.io/api/v0/get_by_name"
    search={
    "apiKey": REMNOT_API,
    "userId":USER_ID,
    "name":datetime.date.today().strftime('%d/%m/%Y')}
    res = requests.post(url_get_by_name, data=search)
    if res.json()["found"] == True:
        return res.json()["_id"]
    else:
        url_get_by_name = "https://api.remnote.io/api/v0/get_by_name"
        search={ "apiKey": REMNOT_API, 
                "userId":USER_ID, 
                "name":'Daily Documents'} 
        res = requests.post(url_get_by_name, data=search) 
        url="https://api.remnote.io/api/v0/create" 
        par={ "apiKey":REMNOT_API, 
                    "userId":USER_ID, 
                    "text": "Temporary" + " #[[" +  str(today) + "]]", 
                    "positionAmongstSiblings" : 0, 
                    "isDocument" : True, 
                    "parentId":res.json()["_id"]
                    } 
        created_rem = requests.post(url, data=par) 
        delete = { "apiKey": REMNOT_API, 
                        "userId":USER_ID, 
                        "remId" : created_rem.json()['remId'] 
                        } 
        delete_url = "https://api.remnote.io/api/v0/delete" 
        requests.post(delete_url, data=delete) 
        search['name'] = datetime.date.today().strftime('%d/%m/%Y') 
        res = requests.post(url_get_by_name, data=search)
        return res.json()["_id"]

############## Save Data to SQL ####################
def account_set_up(update, context):
    global chat_id
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Hi, I am RemNote Telegram Bot")
    context.bot.send_message(chat_id=update.effective_chat.id, text = "My main purpose is to be a sort of webclipper")
    context.bot.send_message(chat_id=update.effective_chat.id, text = "You can send me notes or weblinks, followed by tags and references and I will try by best to save them to the RemNote")
    context.bot.send_message(chat_id=update.effective_chat.id, text = "But let's make some initial configuration at first")
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Please send me API key")
    return THIRD

def api_set(update, context):
    global api
    api =  update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Great, now please send me your UserId")
    return FOURTH

def user_id_set(update, context):
    global userid, api, chat_id, df, DATABASE_URL
    DATABASE_URL = os.environ['DATABASE_URL']
    engine = create_engine(DATABASE_URL)
    df = pd.read_sql_query('select chatid, api, userid from "ids"',con=engine)
    userid =  update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Fantastic!")
    columns = list(df.columns) 
    if chat_id not in list(df[columns[0]]):
        df = df.append(pd.DataFrame({
                columns[0]:[chat_id],
                columns[1]:[api],
                columns[2]:[userid]
                }))
    df.to_sql('ids', engine, if_exists='replace', index=False)
    engine.dispose()
    context.bot.send_message(chat_id=update.effective_chat.id, text = "All set up!")
    return FIRST
############## Saving to RemNote #####################

# Start the conversation 

def start_doc(update, context):
    global DOCUMENT, LINK, MEDIA_ID
    DOCUMENT = True
    LINK = False
    media = context.bot.get_file(update.message.document)
    photo = context.bot.get_file(media.file_id)
    MEDIA_ID = media.file_id
    photo.download(f"{media.file_id}.pdf")
    if PARENT != None:
        send_note(text=update.message.text, parent=PARENT, doc=media.file_id)
    else:
        update.message.reply_text("Need some extra details...",
            reply_markup=main_menu_keyboard())
        return FIRST

def start(update, context):
    """Echo the user message."""
    global LINK, DOCUMENT, NOTE, PARENT, URL, df, REMNOT_API, USER_ID, DATABASE_URL
    DATABASE_URL = os.environ['DATABASE_URL']
    engine = create_engine(DATABASE_URL)
    df = pd.read_sql_query('select chatid, api, userid from "ids"',con=engine)
    engine.dispose()
    columns = list(df.columns)
    df = df.astype({columns[0]: int, columns[1]: str, columns[2]:str})
    if int(update.effective_chat.id ) in list(df[columns[0]]):
        REMNOT_API = str(list(df[df[columns[0]] ==int(update.effective_chat.id) ][columns[1]])[0])
        USER_ID = str(list(df[df[columns[0]] ==int(update.effective_chat.id) ][columns[2]])[0])
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Please make an intial setup first with /start command")
        return ConversationHandler.END
    DOCUMENT = False
    NOTE = update.message.text
    try:
        text_to_search = str(NOTE).rsplit()
        URL=None
        for i in text_to_search:
            if URL != None:
                break
            else:
                try:
                    URL = re.search("(?P<url>https?://[^\s]+)", str(i)).group("url")
                except:
                    pass
        requests.get(URL)
        LINK = True
    except:
        LINK = False
    if PARENT != None:
        send_note(text=update.message.text, parent=PARENT)
    else:
        update.message.reply_text("Need some extra details...",
            reply_markup=main_menu_keyboard())
        return FIRST

def search_parent():
    global HOME_DIR, REMNOT_API, USER_ID
    name = HOME_DIR
    url_get_by_name = "https://api.remnote.io/api/v0/get_by_name"
    search={
    "apiKey": REMNOT_API,
    "userId":USER_ID,
    "name":name}
    res = requests.post(url_get_by_name, data=search)
    if res.json()['found'] == True:
        return res.json()['_id']
    else:
        url_post="https://api.remnote.io/api/v0/create"
        par={
            "apiKey": REMNOT_API,
            "userId":USER_ID,
            "text": name ,
            "isDocument" : True
            }
        created_rem = requests.post(url_post, data=par)
        return created_rem.json()['remId']

# First menu hangling
def daily_docs(update, context):
    """Echo the user message."""
    global LINK, DOCUMENT, NOTE, NOTE_ID    
    query = update.callback_query
    query.answer()
    NOTE_ID = send_note(text=NOTE, link=LINK)
    query.edit_message_text(text = first_menu_message(), 
                        reply_markup=first_menu_keyboard())
    return SECOND


def separate_dir(update, context):
    """Echo the user message."""
    global LINK, DOCUMENT, NOTE, NOTE_ID, today
    query = update.callback_query
    query.answer()
    NOTE_ID = send_note(text=NOTE + "#[["+today+"]]", link=LINK, parent=search_parent())
    query.edit_message_text(text = first_menu_message(),
                         reply_markup=first_menu_keyboard())
    return SECOND


# Second menu hangling
def update_rem(update, context):
    """Echo the user message."""
    global PARENT, NOTE_ID
    PARENT = NOTE_ID
    query = update.callback_query
    query.answer()
    query.edit_message_text("When you done adding notes, please type /stop command")
    return ConversationHandler.END

def stop_conv(update, context):
    """Echo the user message."""
    query = update.callback_query
    query.answer()
    query.edit_message_text("Sure.")
    return ConversationHandler.END

# Stop notes adding
def stop(update, context):
    """Echo the user message."""
    global PARENT
    PARENT=None
    DOCUMENT = False
    LINK = False

# Menus
def main_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(main_menu_message(),
                            reply_markup=main_menu_keyboard())
    return FIRST


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Save to daily notes', callback_data='daily_docs')],
                [InlineKeyboardButton('Save to separate dir', callback_data='separate_dir')]]
    return InlineKeyboardMarkup(keyboard)

def first_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Yes', callback_data='update_rem')],
                [InlineKeyboardButton('No', callback_data='stop')]]
    return InlineKeyboardMarkup(keyboard)

def main_menu_message():
  return 'Where to save?:'

def first_menu_message():
  return 'Add some additional notes? (inside created rem):'

# Error messages
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    global PARENT
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.text, start), 
            MessageHandler(Filters.document, start_doc)
            ],
        states={
            FIRST: [
                CallbackQueryHandler(main_menu, pattern='main'),
                CallbackQueryHandler(daily_docs, pattern='daily_docs'),
                CallbackQueryHandler(separate_dir, pattern='separate_dir'),
            ],
            SECOND: [
                CallbackQueryHandler(update_rem, pattern="update_rem"),
                CallbackQueryHandler(stop_conv, pattern="stop"),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )
    conv_handler2 = ConversationHandler(
        entry_points=[
            CommandHandler("start", account_set_up)
            ],
        states={
            THIRD: [
                MessageHandler(Filters.text, api_set),
            ],
            FOURTH: [
                MessageHandler(Filters.text, user_id_set),            ],
        },
        fallbacks=[CommandHandler("start", account_set_up)],
    )
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(conv_handler2)
    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=TOKEN)
    updater.bot.setWebhook(HEROKU_NAME + TOKEN)
    updater.idle()
if __name__ == '__main__':
    main()
