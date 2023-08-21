from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from time import sleep


api_id = '26588107'
api_hash = 'eb330f0a382b11c976d1866744b94606'
session_string = '1aaNk8EX-YRfwoRsebUkugFvht6DUPi'
# channel_username = 'makarenko_channel'
# channel_username = 'ithumor'

async def get_channel_messages(search_text, channel_username = None, limit=10):
    print(search_text, search_text, limit)
    client = TelegramClient('bot', api_id, api_hash)
    
    await client.start()
    # Find the channel by its username
    channel = await client.get_entity(channel_username)
    
    last_msg_id = -1
    # find Last msg id
    async for message in client.iter_messages(channel, search=search_text, reverse=False, limit=1):
        last_msg_id = message.id

    await client.disconnect()

    messages = []
    offset_id = 0
    while offset_id <= last_msg_id:
        # async for message in client.iter_messages(channel, reverse=True, limit=5):
        # async for message in client.iter_messages(None, search='uzauto'):
        await client.start()
        async for message in client.iter_messages(channel, search='hello',reverse=True, offset_id=offset_id, limit=limit):
            messages.append(message)
        await client.disconnect()
        
        # save last read msg id
        offset_id = messages[-1].id
        
        # avoid BAN
        sleep(1)
        
        # end
        if offset_id == last_msg_id:
            break
    return messages
    # messages = client.loop.run_until_complete(get_channel_messages(channel_username, search_text))

# to test (run as a script)
# import asyncio
# asyncio.run(get_channel_messages('hello', 'ithumor', 3))

        