# Background

This is a telegram bot, that sends text notes to the daily documents (or in a separate folder, just tagging date) in [remnote](https://www.remnote.io/). If the text contains a link, then this link will be extracted and used as a source for rem. Any additional notes, following the created rem, are possible.

The bot is intended to be run from [heroku](https://heroku.com) on a free tier. The installation guide below describes how to get the bot running.

# Features
1. **Send text notes** directly to the daily page, or in a separate folder, still referencing today's page
2. **Share websites** to the remnote (the same as text notes). If a link is found within the text, then it becomes a source, and page title becomes the rem text
3. **Add** any subsequent **notes to the created** rem (right after the creation). All the notes will put inside created rem. 
4. **Tags** are only supported if they are one word ( underscore delimiter can be also used). In this case they can be added via ##example_tag while making a note. **You can add multi-word tags via #[[example tag]]**
5. **References** are encapsulated in [[example reference]]. They can consist of several words. 
6. **Send photos** in the same way as text notes! 
7. **Embed audios or voice messages** in the daily notes or in a separate folder
8. **Embed videos** by sending bideo file, or a link. If you are sending a link the additional question will be asked if this link is a video link (for example to youtube video) 
9. **Make your text stands**! You can use [this](https://forum.remnote.io/t/ability-to-create-all-content-via-api-and-remnote-flavored-markdown-paste-syntax/310) guide to make your tect **bold** or add some headers!

**For example**: The one can share a link to a bot and follow it with several text messages, describing the ideas described in the website. Maybe "##Idea" can be tagged or [[example project]] referenced.


# Installation

1. Create a new bot via the @BotFather bot in Telegram. Just type `/newbot` command and follow the instructions
2. Install [Git](https://git-scm.com/downloads) and [Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)
3. Clone this repo locally and go to the folder. Just type in terminal (or git bash) `git clone && cd` 
4. Then initialize an empty repo `git init`
5. Create a Heroku app.
   1. `heroku login` <- login to the Heroku CLI. If you don't have an account on Heroku, create one.
   2. `heroku create` <- create an app
6. Make API key for remnote (Make sure you registered in RemNote (; )). Please go [here](https://www.remnote.io/api_keys) and add a new API key. **Leave** "Enter the name of the top-level folder to restrict this API key to. (Leave this empty for full access.)" field **empty**. Then Name the Key as you wish. 
7. Open `bot.py` file in any text editor (in a locally cloned copy of a repo) and add the following fields:
   1. `TOKEN = ''` <- This is Telegram bot token. It must have been given from @BotFather bot. To remind it, you can list created bots via `/mybots`  -> `<your-bot-name>` -> `API Token` 
   2. `REMNOT_API= ''` <- This is created RemNote API key (in step 6).
   3. `USER_ID = ''` <- User Id can be obtained from [this](https://www.remnote.io/api_keys) page, where you have created your RemNote API. Copy the value from `User ID` column.
   4. `HEROKU_NAME = ''` <- is the name of your Heroku app when you typed `heroku create`. Paste it in the format `https://yourherokuappname.herokuapp.com/`.
   5. `HOME_DIR = 'Saved Telegram'` <- Name of a directory (rem) where to save content. You can provide any name you want. If no Rem will be found, it will be created
8. Save the `bot.py` file. 
9. From a terminal in a repo directory type `heroku git:remote -a YourAppName`, where your app name should be obtained from the created link - `https://yourherokuappname.herokuapp.com/`
10. Type `git push heroku master`
11. (optional) Go to the @BotFather bot in a Telegram. Go to the `/mybots`  -> `<your-bot-name>` -> `Edit Bot` -> `Edit Command` and type `stop - stop adding notes`. Then in the same `Edit Bot` menu go to the `Edit Botpic` and upload the picture you like. I used [this](https://drive.google.com/file/d/1_6PxFeHHWRDj26UIpuwcUsKam_FN6XSv/view) official one. All the official materials are available [here](https://www.remnote.io/a/remnote-media-kit/5fd4ff11c3785c0045946db7)
12. Congrats, all is done!

# Usage

The only input, that is needed from the user, is a sent text message. Then the conversation dialogue via incline keyboard will begin:
1. Firstly, the user can choose if to save note directly to the daily document, or save it separately
2. If a link is provided, then the bot will ask you if you intended to embed a video (additional dialog)
3. Secondly, the user can add some following notes. You can add as many notes as you wish. Every message will be treated as separate rem. Links will not be extracted in this mode and would be treated as text. If you finished adding notes, then send the `/stop` command.

Everything regarding how to use tags and references is in the **Features** section. If any API changes will be made, then this bot will change and evolve (:

# What free Heroku tier means
Because the bot is hosted on a free Heroku tier, it will go asleep after 30 min of inactivity. What that really means is that it can take up to 1 min for the bot to wake up after sending a message (after a long inactivity period). To my mind, it makes no big deal, but if it bothers you, then you can use [Kaffeine](https://kaffeine.herokuapp.com) app. But do not forget then to add some more free [dynos](https://www.heroku.com/dynos) (+400) via adding a credit card to your account! 
