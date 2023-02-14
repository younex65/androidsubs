import telegram
import requests

# Set up your Telegram bot token
bot = telegram.Bot(token='5946773614:AAFav80hTQL7nO7OxAYBJpH7Ipp0tn6ryuc
')

# Set up your Outline API URL and API key
outline_url = 'https://91.107.168.225:43725/CQfbItBsL_hqxCedsPug-g'
outline_api_key = '3FF642843D71FE90900FDF43C2757EB244745261FECDA4C62508BEEBFAE67637'

# Define function to handle incoming messages
def handle_message(update, context):
    message = update.message.text.lower()
    chat_id = update.message.chat_id
    
    if message.startswith('/adduser'):
        # Parse message to get user email and password
        _, email, password = message.split()
        
        # Call Outline API to add user
        response = requests.post(f'{outline_url}/add_user', headers={'Authorization': outline_api_key},
                                 json={'email': email, 'password': password})
        
        # Send message to user
        bot.send_message(chat_id=chat_id, text=response.json()['msg'])
        
    elif message.startswith('/removeuser'):
        # Parse message to get user ID
        _, user_id = message.split()
        
        # Call Outline API to remove user
        response = requests.post(f'{outline_url}/remove_user', headers={'Authorization': outline_api_key},
                                 json={'user_id': user_id})
        
        # Send message to user
        bot.send_message(chat_id=chat_id, text=response.json()['msg'])
        
    elif message.startswith('/listusers'):
        # Call Outline API to get list of users
        response = requests.get(f'{outline_url}/list_users', headers={'Authorization': outline_api_key})
        
        # Send message to user with list of users
        users = response.json()['users']
        user_list = '\n'.join([f"{user['id']}: {user['email']}" for user in users])
        bot.send_message(chat_id=chat_id, text=user_list)
        
    else:
        bot.send_message(chat_id=chat_id, text='Invalid command. Please use /adduser, /removeuser, or /listusers.')
        
# Set up a message handler and start the bot
updater = telegram.ext.Updater(token='your_bot_token_here')
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
updater.start_polling()
updater.idle()
