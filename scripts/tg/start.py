from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from time import sleep
import dto
from domain import models
from domain.database_models.enums import SearchStatus
api_id = '26588107'
api_hash = 'eb330f0a382b11c976d1866744b94606'
session_string = '1aaNk8EX-YRfwoRsebUkugFvht6DUPi'

async def get_channel_messages(search:dto.SearchDTO):
    print(search.word, search.telegram_channel, search.telegram_limit)
    client = TelegramClient('bot', api_id, api_hash)
    
    await client.start()
    # Find the channel by its username
    try:
        channel = await client.get_entity(search.telegram_channel)
    except:
        print('no channel by this name')
        return False 

    search_obj = await models.Search.get_or_none(id=search.id)
    search_obj.status = SearchStatus.PARSING
    await search_obj.save()

    last_msg_id = -1
    # find Last msg id
    async for message in client.iter_messages(channel, search=search.word, reverse=False, limit=1):
        last_msg_id = message.id

    await client.disconnect()

    messages = []
    offset_id = 0
    while offset_id <= last_msg_id:
        await client.start()
        async for message in client.iter_messages(channel, search=search.word, reverse=True, offset_id=offset_id, limit=search.telegram_limit):
            messages.append(message)
            print(message)
        await client.disconnect()
        
        # save last read msg id
        offset_id = messages[-1].id
        
        # avoid BAN
        sleep(1)
    
        # end
        if offset_id == last_msg_id:
            break

    # post_obj = await models.Post.create(
    #     search = search_obj,
    #     author = 
    #     text = fields.TextField(null=True)
    #     url = fields.CharField(max_length=1000)
    #     media = fields.JSONField(null=True)
    #     date = fields.DatetimeField(null=True)
    #     top_three_emoji = fields.JSONField(null=True)
    #     shares = fields.IntField(null=True, default=0)
    #     comments_count = fields.IntField(null=True, default=0)
    #     status = fields.CharEnumField(enum_type=AnalizeStatus)#
    #     data = fields.JSONField(null=True)
    #     tone = fields.CharField(max_length=100, null=True)#
    #     summary = fields.CharField(max_length=500, null=True)#
    #     search_id:uuid.UUID
    #     comments: fields.ReverseRelation["models.Comment"]
    #     )

        