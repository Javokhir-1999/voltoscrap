from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from time import sleep
import uuid
import json

import dto
from domain import models
from domain.database_models.enums import SearchStatus, AnalizeStatus, Source

# Replace these with your own values
api_id = '26588107'
api_hash = 'eb330f0a382b11c976d1866744b94606'
session_string = '1aaNk8EX-YRfwoRsebUkugFvht6DUPi'
# Create a Telethon client
client = TelegramClient('bot', api_id, api_hash)

async def get_channel_messages(search: dto.SearchDTO):
    await client.start()

    if search.telegram_channels:
        for channel_username in search.telegram_channels.split(','):

            try:
                channel = await client.get_entity(channel_username)
                print(channel)
            except Exception as ex:
                print(ex)
                continue

            for text in search.words.split(','):
                print(text, channel_username)

                last_msg_id = -1
                # find Last msg id
                async for message in client.iter_messages(channel, search=text, reverse=False, limit=1):
                    print(message)
                    last_msg_id = message.id

                offset_id = 0
                while offset_id < last_msg_id:
                    async for message in client.iter_messages(channel, search=text, reverse=True, offset_id=offset_id,
                                                              limit=search.telegram_limit):
                        print(message)
                        try:
                            post_obj = await models.Post.create(
                                word=text,
                                source = Source.TG,
                                search_id=search.id,
                                author = channel.title,
                                author_id = channel.username,
                                pos_source_unique_id=message.id,
                                text = message.text,
                                date = message.date,
                                # top_three_emoji = message.reactions,
                                # shares = message.forwards,
                                status = AnalizeStatus.NEW
                            )
                        except Exception as e:
                            print('Exception post:',e)
                        # save last read msg id
                        offset_id = message.id

                    print(offset_id, "-", last_msg_id)
                # avoid BAN
                sleep(1)

                # end
                if offset_id == last_msg_id:
                    break
    else:
        for text in search.words.split(','):
            print(text, )

            async for message in client.iter_messages(None, search=text, limit=search.telegram_limit):
                print(message)
                try:
                    author_id = None
                    author = None
                    try:
                        author_id = message.chat.username
                        author = message.chat.title
                    except:
                        pass
                    post_obj = await models.Post.create(
                        word=text,
                        search_id=search.id,
                        author=author,
                        author_id=author_id,
                        pos_source_unique_id=message.id,
                        text=message.text,
                        date=message.date,
                        # top_three_emoji = message.reactions,
                        # shares = message.forwards,
                        status=AnalizeStatus.UNANALIZED
                    )
                except Exception as e:
                    print('Exception post:', e)
                # save last read msg id
                offset_id = message.id

            # avoid BAN
            sleep(1)

    await client.disconnect()
    print('end.')






