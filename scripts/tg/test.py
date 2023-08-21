from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from time import sleep
import uuid
import json

channels_list = [
    'qalampir',
    'Sara_Xabarlar',
    'Tashkent_society',
    'shmirziyoyev',
    'eltuz2022',
    'kunuzofficial',
    'Jx_uzb',
    'qalampir',

]
text_list = [
    "Shavkat Umurzakov",
    "Shavkat Umurzoqov",
    "Sh. Umurzakov",
    "Sh. Umurzoqov",
    "Sh.Umurzakov",
    "Sh.Umurzoqov",
    "Ш. Умурзоқов",
    "Ш. Умурзаков",
    "Шавкат Умурзаков",
    "Шавкат Умурзоқов",
    "Shavkat Bo'ronovich Umurzoqov",
    "Shavkat Buranovich Umurzakov",
    "Shavkat Bo'ronovich",
    "Shavkat Umurzoqov",
    "Shavkat Buranovich",
    "Shavkat Umurzakov",
    "Bo'ronovich Umurzoqov",
    "Buranovich Umurzakov",
    "Шавкат Буранович Умурзаков",
    "Шавкат Бўронович Умурзоқов",
    "Шавкат Буранович",
    "Шавкат Умурзаков",
    "Шавкат Бўронович",
    "Шавкат Умурзоқов",
    "Буранович Умурзаков",
    "Бўронович Умурзоқов",
    "Toshkent Shahar Hokimligi",
    "Toshkent Shaxar Hokimligi",
    "Toshkent Shaxar Xokimligi",
    "TOSHKENT SHAHAR HOKIMIYATI",
    "Тошкент шаҳар ҳокимлиги",
    "Тошкент шахар ҳокимлиги",
    "Тошкент шахар хокимлиги",
    "ТОШКЕНТ ШАҲАР ҲОКИМИЯТИ"
]

# Replace these with your own values
api_id = '26588107'
api_hash = 'eb330f0a382b11c976d1866744b94606'
session_string = '1aaNk8EX-YRfwoRsebUkugFvht6DUPi'
# channel_username = 'makarenko_channel'
# channel_username = 'Tezkor_Xabarlar_Yangiliklar_24'
# channel_username = None

# Create a Telethon client
client = TelegramClient('bot', api_id, api_hash)


async def get_channel_messages(text, channel_username):
    from datetime import datetime
    await client.start()

    if channel_username:
        # Find the channel by its username
        channel = await client.get_entity(channel_username)
    else:
        channel = None

    last_msg_id = -1
    # find Last msg id
    async for message in client.iter_messages(channel, search=text, reverse=False, limit=1):
        last_msg_id = message.id

    messages = []
    offset_id = 0
    while offset_id <= last_msg_id:
        # async for message in client.iter_messages(channel, reverse=True, limit=5):
        # async for message in client.iter_messages(None, search='uzauto'):
        async for message in client.iter_messages(channel, search=text, reverse=True, offset_id=offset_id, limit=500):
            # print(message)

            reactions = None
            if message.reactions:
                print(message.reactions)
                reactions = message.reactions.results
            now = datetime.now()
            messages.append({
                'source': 'tg',
                'post':
                    {
                        'post_id': message.id,
                        'author_id': message.from_id,
                        'text': message.text,
                        'emojis': reactions,
                        'replies': None,
                        'replied_to': message.reply_to,
                        'media': None,
                        'posted_date': str(message.date),
                        'translated_text': '',
                        'summarized_text': '',
                        'tone': 0,
                    },
                'gathered_date': now.strftime("%d/%m/%Y %H:%M"),
                'url': '',

            })

        # save last read msg id
        if any(messages):
            offset_id = messages[-1]['post']['post_id']
        else:
            print('no results')
            break

        print(offset_id, "-", last_msg_id)

        # avoid BAN
        sleep(2)

        if offset_id == last_msg_id:
            break

    await client.disconnect()
    return messages


if __name__ == '__main__':
    for channel_username in channels_list:
        for text in text_list:
            messages = client.loop.run_until_complete(get_channel_messages(text, channel_username))

            if any(messages):
                print(messages)
                json_object = json.dumps(messages, indent=4, ensure_ascii=False)
                with open("test.json", 'a', encoding='utf-8') as outfile:
                    json.dump(messages, outfile, indent=4, ensure_ascii=False)




