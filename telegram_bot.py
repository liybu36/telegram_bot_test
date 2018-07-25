import requests
import datetime
from pprint import pprint

class BotHandler():
    def __init__(self,token):
        #token = '694961118:AAE5JvPpWmm-qW_DttrMqycekXk0yUFn03I'
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):  
        method = 'getUpdates'
        params = {'timeout':timeout, 'offset':offset}
        response = requests.get(self.api_url+method,data=params)
        if response.status_code == 200:
            #return response.text
            return response.json()['result']
        return None

    def get_last_update(self):
        results = self.get_updates()
        if len(results) > 0:
            return results[-1]
        else:
            return results[len(results)]

    def get_chat_id(self,update):
        chat_id = update['message']['chat']['id']
        return chat_id

    def send_message(self, chat_id, text):
        params = {'chat_id':chat_id, 'text':text}
        response = requests.post(self.api_url+'sendMessage',data=params)
        return response


def main():
    token = '694961118:AAE5JvPpWmm-qW_DttrMqycekXk0yUFn03I'
    greet_bot = BotHandler(token)

    greetings = ['hello', 'hi', 'greetings', 'sup']
    now = datetime.datetime.now()

    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']        

        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_message(last_chat_id, 'Good Morning  {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_message(last_chat_id, 'Good Afternoon {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            greet_bot.send_message(last_chat_id, 'Good Evening  {}'.format(last_chat_name))
            today += 1

        new_offset = last_update_id + 1


"""
    update_id = last_update(get_updates_json(url))['update_id']
    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:
            message = send_mess(get_chat_id(last_update(get_updates_json(url))),text)
            update_id += 1
            pprint(message.json())
            sleep(1)
"""            

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()