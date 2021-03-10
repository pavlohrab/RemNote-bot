# Background

![Visitor count](https://shields-io-visitor-counter.herokuapp.com/badge?page=pavlohrab.RemNote-bot&style=for-the-badge)
![GitHub](https://img.shields.io/github/license/pavlohrab/RemNote-bot?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/pavlohrab/RemNote-bot?style=for-the-badge)
![GitHub Repo stars](https://img.shields.io/github/stars/pavlohrab/RemNote-bot?style=for-the-badge)
![GitHub contributors](https://img.shields.io/github/contributors/pavlohrab/RemNote-bot?style=for-the-badge)

This is a telegram bot, that sends text notes to the daily documents (or in a separate folder, just tagging date) in [remnote](https://www.remnote.io/). If the text contains a link, then this link will be extracted and used as a source for rem. Any additional notes, following the created rem, are possible.

The bot is intended to be run from [heroku](https://heroku.com) on a free tier. The installation guide below describes how to get the bot running.

# How to use this example!
This is an example bot, to play with. For the purpose of this bot testing only remnote account and bot was created

**Note: Do not put any sensitive information via this bot! The whole world have access to it!! Any text as "test" or "Hello" would be enough(:**

The Remnote testing account credentials:
Username: `TESTING_ONLY`
Password: `RvP8@tgvJX9nM41T!cPtc8Lg3`

The example bot for testing can be found in telegram by username: `@RemNote_example_bot`

All the information, except Heroku app is already in the bot. The user should only whether configure the heroku account, or run the bot locally (preferred)

The initially bot is intended to be run locally via terminal or command prompt with `python bot.py` command. Prior to run the one should install required libraries with pip (should be already in your system if Python is installed. If not, then please install python) `pip install bs4 telegram requests datetime` via terminal or command prompt.

If you would like to run the bot on HEROKU server, please use the following commenting pattern for the lines below
```python
#    updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=TOKEN)
    updater.bot.setWebhook(HEROKU_NAME + TOKEN)
```
By default the `updater.start_pooling()` is uncomented (so used), while `updater.start_webhook` and `updater.bot.setWebhook` are commented

# Features
1. **Send text notes** directly to the daily page, or in a separate folder, still referencing today's page
2. **Share websites** to the remnote (the same as text notes). If a link is found within the text, then it becomes a source, and page title becomes the rem text
3. **Add** any subsequent **notes to the created** rem (right after the creation). All the notes will put inside created rem. 
4. **Tags** are only supported if they are one word ( underscore delimiter can be also used). In this case they can be added via ##example_tag while making a note.
5. **References** are encapsulated in [[example reference]]. They can consist of several words. 
6. **Send photos** in the same way as text notes! 

**For example**: The one can share a link to a bot and follow it with several text messages, describing the ideas described in the website. Maybe "##Idea" can be tagged or [[example project]] referenced.

# Usage

The only input, that is needed from the user, is a sent text message. Then the conversation dialogue via incline keyboard will begin:
1. Firstly, the user can choose if to save note directly to the daily document, or save it separately
2. Secondly, the user can add some following notes. You can add as many notes as you wish. Every message will be treated as separate rem. Links will not be extracted in this mode and would be treated as text. If you finished adding notes, then send the `/stop` command.

Everything regarding how to use tags and references is in the **Features** section. If any API changes will be made, then this bot will change and evolve (: