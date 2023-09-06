from scripts.fb.logic import Facebook
import dto
from domain import models

async def start(search: dto.SearchDTO):
    search_obj = await models.Search.get(id=search.id)
    try:
        fc = Facebook()
        fc.login('abdullajongaybullayev58@gmail.com', '10u&Nf9bVSeP')
        if search.facebook_channels:
            for channel_username in search.facebook_channels.split(','):
                try:
                    fc.redirect_to_channel(channel_username)
                    for text in search.words.split(','):
                        fc.channel_search(text)
                        fc.scroll(search)
                        await fc.get_posts(search)
                        fc.go_back()
                except Exception as ex:
                    print(ex)

        else:
            for text in search.words.split(','):
                fc.global_search(text)
                fc.scroll(search)
                await fc.get_posts(search)

        if search.fb_posts:
            try:
                for post_url in search.fb_posts.split(','):
                    await fc.get_post_by_url(search, post_url)

            except Exception as ex:
                print(ex)

        fc.quit()
    except Exception as e:
        print("FB Exception:")
    await search_obj.recalc_counts()